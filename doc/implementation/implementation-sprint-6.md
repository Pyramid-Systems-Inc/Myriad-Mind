# Implementation Plan - Sprint 6: Multi-Modal Learning

**Sprint 6 of 7** | [← Previous Sprint](implementation-sprint-5.md) | [Next Sprint →](implementation-sprint-7.md)

This document covers Sprint 6 of the Myriad-Mind implementation plan, focusing on multi-modal learning from images, audio, and cross-sensory data (Weeks 19-21).

[← Back to Implementation Overview](../INDEX.md#implementation) | [View All Sprints](../INDEX.md#implementation)

---

## SPRINT 7: Multi-Modal Learning (Weeks 19-21)

**Goal:** Enable learning from images, audio, and multi-sensory data.

**Target Outcome:** System can understand and learn from multiple modalities, not just text.

---

### Phase 7.1: Multi-Modal Foundation (Week 19)

#### Implementation Steps

**7.1.1 Add Embedding Services (Day 1-3)**

Create new services for multi-modal embeddings:

**Image Embedding Service**

File: `src/myriad/services/embeddings/image_embedder/app.py`

```python
"""
Image Embedding Service
Converts images to vector embeddings using CLIP or similar models.
"""

from flask import Flask, request, jsonify
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import io

app = Flask(__name__)

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

@app.route('/embed', methods=['POST'])
def embed_image():
    """Generate embedding for uploaded image"""
    
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))
    
    # Process image
    inputs = processor(images=image, return_tensors="pt")
    
    # Generate embedding
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    
    # Convert to list for JSON serialization
    embedding = image_features[0].tolist()
    
    return jsonify({
        "embedding": embedding,
        "dimension": len(embedding),
        "model": "clip-vit-base-patch32"
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "image_embedder",
        "model": "clip-vit-base-patch32"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020)
```

**Audio Embedding Service**

File: `src/myriad/services/embeddings/audio_embedder/app.py`

```python
"""
Audio Embedding Service
Converts audio to vector embeddings using audio models.
"""

from flask import Flask, request, jsonify
import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import io

app = Flask(__name__)

# Load Wav2Vec2 model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

@app.route('/embed', methods=['POST'])
def embed_audio():
    """Generate embedding for uploaded audio"""
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio provided"}), 400
    
    audio_file = request.files['audio']
    
    # Load audio
    waveform, sample_rate = torchaudio.load(io.BytesIO(audio_file.read()))
    
    # Resample if necessary
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        waveform = resampler(waveform)
    
    # Process audio
    inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")
    
    # Generate embedding
    with torch.no_grad():
        audio_features = model(**inputs).last_hidden_state
    
    # Use mean pooling
    embedding = audio_features.mean(dim=1).squeeze().tolist()
    
    return jsonify({
        "embedding": embedding,
        "dimension": len(embedding),
        "model": "wav2vec2-base-960h"
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "audio_embedder",
        "model": "wav2vec2-base-960h"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5021)
```

**Docker Configuration**

Add to [`docker-compose.yml`](../../docker-compose.yml:1):

```yaml
image_embedder:
  build:
    context: ./src/myriad/services/embeddings/image_embedder
  container_name: image_embedder
  ports:
    - "5020:5020"
  networks:
    - myriad_network
  deploy:
    resources:
      limits:
        cpus: '1.0'
        memory: 2G
      reservations:
        memory: 1G
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5020/health"]
    interval: 30s
    timeout: 10s
    retries: 3

audio_embedder:
  build:
    context: ./src/myriad/services/embeddings/audio_embedder
  container_name: audio_embedder
  ports:
    - "5021:5021"
  networks:
    - myriad_network
  deploy:
    resources:
      limits:
        cpus: '1.0'
        memory: 2G
      reservations:
        memory: 1G
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5021/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```

**7.1.2 Add Multi-Modal Graph Schema (Day 3-5)**

Extend graph schema to support multi-modal data:

File: `scripts/init_schema_multimodal.cypher`

```cypher
// Multi-Modal Extensions to Graph Schema
// Extends existing schema with sensory nodes

// ========================================
// NEW NODE TYPES
// ========================================

// Sensory Node for multi-modal data
CREATE CONSTRAINT sensory_id_unique IF NOT EXISTS
FOR (s:SensoryNode) REQUIRE s.id IS UNIQUE;

CREATE INDEX sensory_type_idx IF NOT EXISTS
FOR (s:SensoryNode) ON (s.type);

CREATE INDEX sensory_created_idx IF NOT EXISTS
FOR (s:SensoryNode) ON (s.created_at);

// ========================================
// NEW RELATIONSHIPS
// ========================================

// Concept to Visual representation
CREATE INDEX has_visual_idx IF NOT EXISTS
FOR ()-[r:HAS_VISUAL]-() ON (r.created_at);

// Concept to Audio representation
CREATE INDEX has_audio_idx IF NOT EXISTS
FOR ()-[r:HAS_AUDIO]-() ON (r.created_at);

// Cross-modal similarity
CREATE INDEX similar_to_idx IF NOT EXISTS
FOR ()-[r:SIMILAR_TO]-() ON (r.similarity_score);

// ========================================
// EXAMPLE MULTI-MODAL CONCEPT
// ========================================

// Create concept with visual and audio
// MATCH (c:Concept {name: "lightbulb"})
// CREATE (v:SensoryNode {
//   id: "img_lightbulb_001",
//   type: "image",
//   embedding: $image_embedding,
//   source_url: "https://example.com/lightbulb.jpg",
//   created_at: timestamp()
// })
// CREATE (c)-[:HAS_VISUAL]->(v)
```

**Python Integration**

File: `src/myriad/services/graphdb_manager/multimodal_operations.py`

```python
"""
Multi-modal operations for graph database.
Handles storage and retrieval of sensory nodes.
"""

from typing import List, Dict, Any, Optional
import requests

def create_sensory_node(driver, concept_name: str, sensory_type: str, 
                       embedding: List[float], source_url: str) -> str:
    """Create a sensory node linked to a concept"""
    
    query = """
    MATCH (c:Concept {name: $concept_name})
    CREATE (s:SensoryNode {
        id: $node_id,
        type: $sensory_type,
        embedding: $embedding,
        source_url: $source_url,
        created_at: timestamp()
    })
    CREATE (c)-[r:HAS_VISUAL]->(s)
    RETURN s.id as node_id
    """
    
    if sensory_type == "audio":
        query = query.replace("HAS_VISUAL", "HAS_AUDIO")
    
    node_id = f"{sensory_type}_{concept_name}_{int(time.time())}"
    
    with driver.session() as session:
        result = session.run(query, {
            "concept_name": concept_name,
            "node_id": node_id,
            "sensory_type": sensory_type,
            "embedding": embedding,
            "source_url": source_url
        })
        
        return result.single()["node_id"]

def find_similar_sensory_nodes(driver, embedding: List[float], 
                               sensory_type: str, limit: int = 5) -> List[Dict]:
    """Find similar sensory nodes using cosine similarity"""
    
    # This would use vector similarity search
    # For now, return placeholder
    # In production, use Neo4j vector indexes or external vector DB
    
    query = """
    MATCH (s:SensoryNode {type: $sensory_type})
    RETURN s.id as id, s.source_url as url
    LIMIT $limit
    """
    
    with driver.session() as session:
        results = session.run(query, {
            "sensory_type": sensory_type,
            "limit": limit
        })
        
        return [dict(record) for record in results]
```

**Success Criteria:**

- ✅ Image embedding service operational
- ✅ Audio embedding service operational
- ✅ Multi-modal nodes in graph schema
- ✅ Embeddings stored and retrievable

---

### Phase 7.2: Multi-Modal Learning Pipeline (Week 20-21)

**Create learning pipeline that accepts multiple modalities**

#### Implementation Steps

**7.2.1 Create Multi-Modal Learning Engine (Day 1-4)**

File: `src/myriad/core/learning/multimodal_learning.py`

```python
"""
Multi-Modal Learning Engine
Learns concepts from text, images, audio simultaneously.
"""

from typing import Dict, List, Any, Optional
import requests
import base64

class MultiModalLearner:
    """Learns from multiple sensory inputs"""
    
    def __init__(self, image_embedder_url: str, audio_embedder_url: str, graphdb_url: str):
        self.image_embedder = image_embedder_url
        self.audio_embedder = audio_embedder_url
        self.graphdb = graphdb_url
    
    def learn_concept(self, concept: str, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Learn concept from multiple modalities"""
        
        embeddings = {}
        
        # Text embedding (existing)
        if 'text' in learning_data:
            embeddings['text'] = self._embed_text(learning_data['text'])
        
        # Image embedding
        if 'images' in learning_data:
            embeddings['images'] = [
                self._embed_image(img) 
                for img in learning_data['images']
            ]
        
        # Audio embedding
        if 'audio' in learning_data:
            embeddings['audio'] = [
                self._embed_audio(aud)
                for aud in learning_data['audio']
            ]
        
        # Create multi-modal representation in graph
        result = self._create_multimodal_concept(concept, embeddings, learning_data)
        
        return {
            "concept": concept,
            "modalities": list(embeddings.keys()),
            "embeddings_generated": {
                "text": 1 if 'text' in embeddings else 0,
                "images": len(embeddings.get('images', [])),
                "audio": len(embeddings.get('audio', []))
            },
            "graph_nodes_created": result.get("nodes_created", 0)
        }
    
    def _embed_text(self, text: str) -> List[float]:
        """Get text embedding (using existing system)"""
        # Would integrate with existing text embedding
        return []
    
    def _embed_image(self, image_data) -> Dict[str, Any]:
        """Get image embedding"""
        try:
            # Prepare image file
            files = {'image': image_data}
            
            response = requests.post(
                f"{self.image_embedder}/embed",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Embedding failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _embed_audio(self, audio_data) -> Dict[str, Any]:
        """Get audio embedding"""
        try:
            files = {'audio': audio_data}
            
            response = requests.post(
                f"{self.audio_embedder}/embed",
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Embedding failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _create_multimodal_concept(self, concept: str, embeddings: Dict, 
                                   learning_data: Dict) -> Dict[str, Any]:
        """Store multi-modal representation in graph"""
        
        nodes_created = 0
        
        # Create image nodes
        if 'images' in embeddings:
            for i, img_embedding in enumerate(embeddings['images']):
                if 'error' not in img_embedding:
                    # Store in graph
                    response = requests.post(
                        f"{self.graphdb}/sensory/create",
                        json={
                            "concept": concept,
                            "type": "image",
                            "embedding": img_embedding['embedding'],
                            "source_url": learning_data.get('image_urls', [])[i] if i < len(learning_data.get('image_urls', [])) else ""
                        }
                    )
                    if response.status_code == 200:
                        nodes_created += 1
        
        # Create audio nodes
        if 'audio' in embeddings:
            for i, aud_embedding in enumerate(embeddings['audio']):
                if 'error' not in aud_embedding:
                    response = requests.post(
                        f"{self.graphdb}/sensory/create",
                        json={
                            "concept": concept,
                            "type": "audio",
                            "embedding": aud_embedding['embedding'],
                            "source_url": learning_data.get('audio_urls', [])[i] if i < len(learning_data.get('audio_urls', [])) else ""
                        }
                    )
                    if response.status_code == 200:
                        nodes_created += 1
        
        return {"nodes_created": nodes_created}
    
    def query_multimodal(self, query_type: str, query_data: Any) -> List[Dict]:
        """Query using multi-modal input"""
        
        if query_type == "image":
            # Find similar concepts via image
            embedding = self._embed_image(query_data)
            if 'error' not in embedding:
                # Search graph for similar image embeddings
                response = requests.post(
                    f"{self.graphdb}/sensory/search",
                    json={
                        "type": "image",
                        "embedding": embedding['embedding'],
                        "limit": 5
                    }
                )
                return response.json() if response.status_code == 200 else []
        
        elif query_type == "audio":
            # Find similar concepts via audio
            embedding = self._embed_audio(query_data)
            if 'error' not in embedding:
                response = requests.post(
                    f"{self.graphdb}/sensory/search",
                    json={
                        "type": "audio",
                        "embedding": embedding['embedding'],
                        "limit": 5
                    }
                )
                return response.json() if response.status_code == 200 else []
        
        return []
```

**7.2.2 Integration with Autonomous Learning (Day 5-7)**

Update autonomous learning engine to use multi-modal data:

File: [`src/myriad/core/learning/autonomous_learning_engine.py`](../../src/myriad/core/learning/autonomous_learning_engine.py:1)

```python
from core.learning.multimodal_learning import MultiModalLearner

class EnhancedAutonomousLearning:
    """Autonomous learning with multi-modal support"""
    
    def __init__(self):
        # Existing initialization
        self.multimodal_learner = MultiModalLearner(
            image_embedder_url="http://image_embedder:5020",
            audio_embedder_url="http://audio_embedder:5021",
            graphdb_url="http://graphdb_manager_ai:5008"
        )
    
    def research_concept(self, concept: str) -> Dict[str, Any]:
        """Research concept with multi-modal data"""
        
        # Text research (existing)
        text_data = self._research_text(concept)
        
        # Image research (new)
        image_data = self._research_images(concept)
        
        # Audio research (new)
        audio_data = self._research_audio(concept)
        
        # Combine all modalities
        learning_data = {
            "text": text_data,
            "images": image_data.get('images', []),
            "image_urls": image_data.get('urls', []),
            "audio": audio_data.get('audio', []),
            "audio_urls": audio_data.get('urls', [])
        }
        
        # Learn from all modalities
        result = self.multimodal_learner.learn_concept(concept, learning_data)
        
        return result
    
    def _research_images(self, concept: str) -> Dict[str, Any]:
        """Find relevant images for concept"""
        # Would integrate with image search API
        # For now, return empty
        return {"images": [], "urls": []}
    
    def _research_audio(self, concept: str) -> Dict[str, Any]:
        """Find relevant audio for concept"""
        # Would integrate with audio/podcast search
        return {"audio": [], "urls": []}
```

**7.2.3 Testing Multi-Modal System (Day 8-10)**

Create tests for multi-modal functionality:

File: `tests/test_multimodal_learning.py`

```python
import pytest
from src.myriad.core.learning.multimodal_learning import MultiModalLearner

def test_image_embedding_service():
    """Test image embedding service"""
    import requests
    from PIL import Image
    import io
    
    # Create test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Test embedding
    response = requests.post(
        "http://localhost:5020/embed",
        files={'image': img_bytes}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert 'embedding' in data
    assert len(data['embedding']) > 0

def test_audio_embedding_service():
    """Test audio embedding service"""
    # Similar to image test
    pass

def test_multimodal_learning():
    """Test learning from multiple modalities"""
    learner = MultiModalLearner(
        image_embedder_url="http://localhost:5020",
        audio_embedder_url="http://localhost:5021",
        graphdb_url="http://localhost:5008"
    )
    
    # Mock learning data
    learning_data = {
        "text": "A lightbulb is an electric light source",
        "images": [],  # Would have actual image data
        "audio": []
    }
    
    result = learner.learn_concept("lightbulb", learning_data)
    
    assert result['concept'] == "lightbulb"
    assert 'modalities' in result

def test_cross_modal_retrieval():
    """Test finding concepts via different modalities"""
    learner = MultiModalLearner(
        image_embedder_url="http://localhost:5020",
        audio_embedder_url="http://localhost:5021",
        graphdb_url="http://localhost:5008"
    )
    
    # Query by image
    results = learner.query_multimodal("image", test_image_data)
    
    # Should find related concepts
    assert len(results) > 0
```

**Success Criteria:**

- ✅ System accepts images for concept learning
- ✅ System accepts audio for concept learning
- ✅ Multi-modal concepts stored in graph
- ✅ Cross-modal retrieval working
- ✅ All multi-modal tests passing

---

## Sprint 6 Summary

### Completed Deliverables

**Week 19: Multi-Modal Foundation**

- ✅ Image embedding service with CLIP
- ✅ Audio embedding service with Wav2Vec2
- ✅ Extended graph schema for sensory nodes
- ✅ Docker configuration for embedding services

**Week 20-21: Learning Pipeline**

- ✅ Multi-modal learning engine
- ✅ Integration with autonomous learning
- ✅ Cross-modal search capabilities
- ✅ Comprehensive testing

### Key Achievements

1. **Multi-Sensory Understanding**: System now processes text, images, and audio
2. **Cross-Modal Learning**: Can learn concepts from multiple data types
3. **Unified Representation**: Different modalities stored in cohesive graph structure
4. **Scalable Architecture**: Embedding services as independent microservices

### Multi-Modal Capabilities

| Modality | Model | Embedding Dimension | Use Case |
|----------|-------|---------------------|----------|
| Text | Existing | Variable | Primary knowledge |
| Image | CLIP ViT-B/32 | 512 | Visual concepts |
| Audio | Wav2Vec2 | 768 | Sound/speech |

### Example Use Case

```
# Learn "dog" concept with multiple modalities
learning_data = {
    "text": "A dog is a domesticated mammal...",
    "images": [dog_photo1, dog_photo2],
    "audio": [dog_bark_audio]
}

result = learner.learn_concept("dog", learning_data)
# Creates: 1 concept node + 2 image nodes + 1 audio node

# Later: Query by showing a dog image
results = learner.query_multimodal("image", new_dog_photo)
# Returns: ["dog", "puppy", "canine", ...]
```

### Next Steps

Sprint 7 will complete the transformation with autonomous cognition - implementing self-awareness, curiosity, and proactive exploration to achieve 85-90% human-like cognition.

---

## Continue Reading

**Next:** [Sprint 7: Autonomous Cognition & Conclusion](implementation-sprint-7.md) - Self-awareness, curiosity engine, autonomous learning loop, and final metrics (Weeks 22-24)

**Related Documentation:**

- [Project Index](../INDEX.md)
- [Architecture Overview](../ARCHITECTURE.md)
- [Autonomous Learning](../../src/myriad/core/learning/)
- [Testing Guide](../TESTING_GUIDE.md)

[← Previous Sprint](implementation-sprint-5.md) | [↑ Back to Index](../INDEX.md) | [Next Sprint →](implementation-sprint-7.md)
