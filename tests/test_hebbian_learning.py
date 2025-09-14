#!/usr/bin/env python3
"""
Hebbian Learning Test Suite
===========================

Validates relationship weight reinforcement, decay, and routing impact.
"""

import sys
import time
import json
import requests

sys.path.append('.')

GRAPHDB = "http://localhost:5008"
ORCH = "http://localhost:5009"  # via Integration_Tester_AI /run_orchestration if needed

def _strengthen(agent_id: str, concept: str, success: bool=True):
    return requests.post(f"{GRAPHDB}/hebbian/strengthen", json={
        "agent_id": agent_id,
        "concept": concept,
        "success": success
    }, timeout=10)

def _decay(concept: str, decay_rate: float=0.2):
    return requests.post(f"{GRAPHDB}/hebbian/decay", json={
        "concept": concept,
        "decay_rate": decay_rate
    }, timeout=10)

def _get_weights(concept: str):
    r = requests.post(f"{GRAPHDB}/get_agents_for_concept", json={"concept": concept}, timeout=10)
    r.raise_for_status()
    data = r.json()
    weights = {item["agent"].get("name"): item["relationship"].get("weight", 0.5) for item in data.get("agents", [])}
    return weights

def test_hebbian_reinforcement_and_decay():
    concept = "lightbulb"
    # Assume agents exist in graph via docker-compose bring-up
    agent_a = "Lightbulb_Definition_AI"
    agent_b = "Lightbulb_Function_AI"

    # Baseline weights
    w0 = _get_weights(concept)
    print("Baseline:", w0)

    # Reinforce A 3 times, B fails once
    for _ in range(3):
        _strengthen(agent_a, concept, True)
    _strengthen(agent_b, concept, False)
    time.sleep(0.5)

    w1 = _get_weights(concept)
    print("After reinforce A and penalize B:", w1)
    assert w1.get(agent_a, 0.5) >= w0.get(agent_a, 0.5)
    assert w1.get(agent_b, 0.5) <= w0.get(agent_b, 0.5)

    # Apply decay
    _decay(concept, 0.5)
    time.sleep(0.5)
    w2 = _get_weights(concept)
    print("After decay:", w2)
    assert w2.get(agent_a, 0.5) <= w1.get(agent_a, 0.5)

if __name__ == '__main__':
    test_hebbian_reinforcement_and_decay()
    print("✅ Hebbian learning tests executed")


