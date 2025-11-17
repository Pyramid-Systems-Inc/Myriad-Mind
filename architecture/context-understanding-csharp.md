# Myriad Cognitive Architecture - Context Understanding & Conversation Memory (C#/.NET Edition)

**Architecture Documentation** | [Overview](system-overview-csharp.md) | [Graph Intelligence](graph-intelligence-csharp.md) | [Microservices](microservices-csharp.md)

Human-like context understanding system enabling natural multi-turn conversations, reference resolution, and personalized interactions - all built from scratch in C# without external dependencies (except .NET SDK and optional LLM integrations).

[← Back to Index](../INDEX.md#architecture) | [Graph Intelligence ←](graph-intelligence-csharp.md)

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Human Context Understanding Model](#human-context-understanding-model)
- [Current Capabilities Analysis](#current-capabilities-analysis)
- [Multi-Layer Context Architecture](#multi-layer-context-architecture)
- [Implementation Approaches](#implementation-approaches)
- [Integration with Existing Components](#integration-with-existing-components)
- [Implementation Roadmap](#implementation-roadmap)
- [Example Scenarios](#example-scenarios)
- [Performance Considerations](#performance-considerations)

---

## Executive Summary

### The Challenge

The current Myriad system excels at single-query processing with uncertainty detection and ambiguity resolution, but lacks the conversational memory and contextual carryover that characterizes human cognition.

**Current Limitation:**

```csharp
// Turn 1
User: "What is a lightbulb?"
System: "A device that produces light..."

// Turn 2
User: "Who invented it?"
System: ❌ "I don't understand what 'it' refers to."
```

**Target Behavior:**

```csharp
// Turn 1
User: "What is a lightbulb?"
System: "A device that produces light..."
[Stored: entity="lightbulb", salience=0.9]

// Turn 2
User: "Who invented it?"
[Resolved: "it" → "lightbulb"]
System: ✅ "Thomas Edison invented the lightbulb in 1879..."
```

### Proposed Solution

Implement a **4-layer context system** that provides comprehensive understanding:

1. **Session Context Layer** (Working Memory) - Track immediate conversation state
2. **User Context Layer** (Episodic Memory) - Maintain long-term user profile
3. **World Context Layer** (Semantic Memory) - Provide general knowledge
4. **Discourse Context Layer** - Understand conversation structure

### Key Benefits

- ✅ **Natural Conversations**: Multi-turn dialogue without repeating context
- ✅ **Reference Resolution**: Understand "it", "that", "they" automatically
- ✅ **Personalization**: Learn user preferences over time
- ✅ **Intelligent Routing**: Context-aware agent selection
- ✅ **Conversation Memory**: Remember past interactions

### Technology Stack

**C#/.NET Components:**

- Custom session management using `MemoryCache` or Redis
- Custom graph database extensions (existing Neo4j-inspired implementation)
- Custom reference resolution algorithms
- Optional LLM integration for advanced reasoning

**Zero External Dependencies** (except for optional enhancements):

- ✅ Core context management: Pure C# with `ConcurrentDictionary`
- ✅ Session storage: `MemoryCache` (built-in) or Redis
- ✅ Persistence: Custom graph database (existing)
- ⚠️ Optional: LLM for advanced reference resolution

---

## Human Context Understanding Model

### How Humans Process Context

Human context understanding operates through multiple interconnected cognitive systems:

#### 1. Working Memory (Short-Term Context)

Humans maintain approximately **7±2 items** in active working memory:

- Recent conversation turns (last 3-5 exchanges)
- Active concepts currently being discussed
- Current goals of the conversation
- Pending questions or unresolved topics

**Example:**

```
Turn 1: "What is a lightbulb?"
Turn 2: "Who invented it?"  ← "it" resolves to "lightbulb" from working memory
```

#### 2. Long-Term Memory (Episodic & Semantic)

Humans recall past interactions and general knowledge:

- **Episodic**: Previous conversations with the same person
- **Semantic**: General world knowledge
- **Personal**: User preferences, expertise level

**Example:**

```
Yesterday: User asked detailed quantum mechanics questions
Today: System adjusts for advanced technical level automatically
```

#### 3. Pragmatic Inference (Reading Between the Lines)

Humans infer unstated information:

- Common sense reasoning
- Cultural context
- Situational awareness
- Theory of mind (understanding speaker's intent)

#### 4. Discourse Understanding (Conversation Flow)

Humans track conversation structure:

- Topic coherence and shifts
- Question-answer pairs
- Ellipsis completion
- Anaphora resolution (pronoun references)

### Context Integration Model

```
┌─────────────────────────────────────────────────────────────┐
│                 Human Context Understanding                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐                     │
│  │   Working    │◄───►│  Long-Term   │                     │
│  │   Memory     │     │   Memory     │                     │
│  │  (3-5 turns) │     │  (History)   │                     │
│  └──────┬───────┘     └──────┬───────┘                     │
│         │                     │                              │
│         │    ┌────────────────┴─────┐                       │
│         │    │                      │                       │
│         ▼    ▼                      ▼                       │
│  ┌──────────────┐          ┌──────────────┐               │
│  │  Pragmatic   │◄────────►│  Discourse   │               │
│  │  Inference   │          │Understanding │               │
│  │(Common Sense)│          │(Conv. Flow)  │               │
│  └──────────────┘          └──────────────┘               │
│         │                           │                       │
│         └───────────┬───────────────┘                      │
│                     ▼                                       │
│          ┌─────────────────────┐                           │
│          │  Contextual         │                           │
│          │  Understanding      │                           │
│          └─────────────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Current Capabilities Analysis

### Existing Strengths

The Myriad system already has sophisticated single-query processing:

#### ✅ Enhanced Graph Intelligence

From [`graph-intelligence-csharp.md`](graph-intelligence-csharp.md):

```csharp
public async Task<List<AgentRelevanceScore>> DiscoverAgentsAsync(
    string concept,
    string intent,
    QueryContext? context = null,
    CancellationToken cancellationToken = default)
{
    // Multi-criteria relevance scoring
    // Performance tracking
    // Dynamic clustering
}
```

**Capabilities:**

- Multi-criteria agent relevance scoring
- Context-aware agent selection (basic)
- Performance tracking
- Hebbian learning for agent relationships

**Limitation:** Context is limited to current query metadata only

#### ✅ Ambiguity Resolution

Custom C# implementation with:

- Concept, intent, context, and scope ambiguity detection
- Context-based disambiguation
- Fallback to most likely interpretation

**Limitation:** No automatic history management

### Critical Gaps

| Human Capability | Current Status | Impact |
|-----------------|----------------|---------|
| **Working Memory** | ❌ None | Cannot remember recent turns |
| **Entity Tracking** | ❌ None | Entities not remembered across queries |
| **Reference Resolution** | ❌ None | Cannot resolve "it", "that", "they" |
| **Topic Continuity** | ❌ None | Each query treated independently |
| **User Profiles** | ❌ None | No persistent preferences |
| **Conversation Flow** | ❌ None | No turn sequence understanding |

---

## Multi-Layer Context Architecture

### Architecture Overview

Four interconnected layers mimicking human cognition:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Session Context (Working Memory)                  │
│  ├─ Turn History (Last 10 turns)                            │
│  ├─ Entity Tracker (Active entities with salience)          │
│  ├─ Topic Tracker (Current topics)                          │
│  └─ Goal Stack (User intentions)                            │
│                                                              │
│  Storage: MemoryCache (in-memory) or Redis (distributed)    │
│  TTL: 30-60 minutes                                          │
└─────────────────────────────────────────────────────────────┘
         ↓ Persists to
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: User Context (Episodic Memory)                    │
│  ├─ Conversation History Graph                              │
│  ├─ User Preference Model                                   │
│  ├─ Knowledge Level Tracker                                 │
│  └─ Interaction Pattern Analyzer                            │
│                                                              │
│  Storage: Custom Graph Database (Neo4j-inspired)            │
│  Persistence: Long-term                                      │
└─────────────────────────────────────────────────────────────┘
         ↑ Enriches
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: World Context (Semantic Memory)                   │
│  ├─ Common Sense Knowledge                                  │
│  ├─ Temporal Context (date/time awareness)                  │
│  ├─ Cultural Context                                         │
│  └─ Domain Knowledge (from concept graph)                   │
│                                                              │
│  Storage: Graph Database + Optional Vector Embeddings       │
└─────────────────────────────────────────────────────────────┘
         ↑ Informs
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Discourse Context                                 │
│  ├─ Conversation Flow Analyzer                              │
│  ├─ Topic Transition Detector                               │
│  ├─ Reference Resolution Engine                             │
│  └─ Question-Answer Tracker                                 │
│                                                              │
│  Storage: In-memory during session, persisted to graph      │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Session Context (Working Memory)

**Purpose**: Track immediate conversation state within a single session

**C# Data Model:**

```csharp
namespace Myriad.Core.Context
{
    /// <summary>
    /// Session context representing working memory
    /// </summary>
    public class SessionContext
    {
        public required string SessionId { get; init; }
        public required string UserId { get; init; }
        public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
        public DateTime LastActive { get; set; } = DateTime.UtcNow;
        
        // Turn history (sliding window)
        public LinkedList<ConversationTurn> TurnHistory { get; init; } = new();
        public int MaxTurns { get; init; } = 10;
        
        // Entity tracking
        public ConcurrentDictionary<string, TrackedEntity> EntityTracker { get; init; } = new();
        
        // Topic tracking
        public List<string> ActiveTopics { get; set; } = new();
        public string? CurrentGoal { get; set; }
    }
    
    /// <summary>
    /// Represents a single conversation turn
    /// </summary>
    public record ConversationTurn
    {
        public required int TurnId { get; init; }
        public required string Query { get; init; }
        public string? ResolvedQuery { get; init; }
        public List<string> Concepts { get; init; } = new();
        public Dictionary<string, EntityMention> Entities { get; init; } = new();
        public required string Intent { get; init; }
        public string? ResponseSummary { get; init; }
        public DateTime Timestamp { get; init; } = DateTime.UtcNow;
    }
    
    /// <summary>
    /// Tracked entity with salience scoring
    /// </summary>
    public class TrackedEntity
    {
        public required string Name { get; init; }
        public required string Type { get; init; } // "Concept", "Person", "Location", etc.
        public int FirstMention { get; set; }
        public int LastMention { get; set; }
        public int MentionCount { get; set; }
        public float Salience { get; set; } // 0.0 to 1.0
        public Dictionary<string, object> Attributes { get; init; } = new();
        
        /// <summary>
        /// Increase salience when entity is mentioned
        /// </summary>
        public void Boost(float delta = 0.3f)
        {
            Salience = Math.Min(1.0f, Salience * 0.9f + delta);
            MentionCount++;
        }
        
        /// <summary>
        /// Decay salience when entity is not mentioned
        /// </summary>
        public void Decay(float factor = 0.95f)
        {
            Salience *= factor;
        }
    }
    
    public record EntityMention
    {
        public required string Type { get; init; }
        public float Salience { get; init; }
        public string? ReferentFrom { get; init; } // e.g., "it", "that"
        public int DiscoveredInTurn { get; init; }
    }
}
```

**Session Context Manager Implementation:**

```csharp
namespace Myriad.Core.Context
{
    /// <summary>
    /// Manages session-based context (working memory)
    /// </summary>
    public class SessionContextManager
    {
        private readonly IMemoryCache _cache;
        private readonly ILogger<SessionContextManager> _logger;
        private readonly TimeSpan _sessionTtl;
        
        public SessionContextManager(
            IMemoryCache cache,
            ILogger<SessionContextManager> logger,
            TimeSpan? sessionTtl = null)
        {
            _cache = cache;
            _logger = logger;
            _sessionTtl = sessionTtl ?? TimeSpan.FromMinutes(30);
        }
        
        /// <summary>
        /// Get existing session or create new one
        /// </summary>
        public SessionContext GetOrCreateSession(string userId, string? sessionId = null)
        {
            if (sessionId != null && _cache.TryGetValue<SessionContext>(sessionId, out var existing))
            {
                existing.LastActive = DateTime.UtcNow;
                _cache.Set(sessionId, existing, _sessionTtl); // Extend TTL
                return existing;
            }
            
            // Create new session
            var newSessionId = sessionId ?? $"sess_{userId}_{DateTime.UtcNow:yyyyMMddHHmmss}";
            var session = new SessionContext
            {
                SessionId = newSessionId,
                UserId = userId
            };
            
            _cache.Set(newSessionId, session, _sessionTtl);
            
            _logger.LogInformation(
                "Created new session {SessionId} for user {UserId}",
                newSessionId, userId);
            
            return session;
        }
        
        /// <summary>
        /// Add a new turn to the conversation history
        /// </summary>
        public void AddTurn(string sessionId, ConversationTurn turn)
        {
            if (!_cache.TryGetValue<SessionContext>(sessionId, out var session))
            {
                _logger.LogWarning("Session {SessionId} not found", sessionId);
                return;
            }
            
            // Add turn to history
            session.TurnHistory.AddLast(turn);
            
            // Maintain sliding window
            while (session.TurnHistory.Count > session.MaxTurns)
            {
                session.TurnHistory.RemoveFirst();
            }
            
            // Update entity tracker
            UpdateEntityTracker(session, turn);
            
            // Update last active
            session.LastActive = DateTime.UtcNow;
            _cache.Set(sessionId, session, _sessionTtl);
            
            _logger.LogDebug(
                "Added turn {TurnId} to session {SessionId}",
                turn.TurnId, sessionId);
        }
        
        /// <summary>
        /// Get recent conversation context
        /// </summary>
        public List<ConversationTurn> GetRecentContext(string sessionId, int nTurns = 3)
        {
            if (!_cache.TryGetValue<SessionContext>(sessionId, out var session))
            {
                return new List<ConversationTurn>();
            }
            
            return session.TurnHistory
                .TakeLast(nTurns)
                .ToList();
        }
        
        /// <summary>
        /// Get entity tracker for reference resolution
        /// </summary>
        public ConcurrentDictionary<string, TrackedEntity> GetEntityTracker(string sessionId)
        {
            if (_cache.TryGetValue<SessionContext>(sessionId, out var session))
            {
                return session.EntityTracker;
            }
            
            return new ConcurrentDictionary<string, TrackedEntity>();
        }
        
        /// <summary>
        /// Update entity tracker with new mentions
        /// </summary>
        private void UpdateEntityTracker(SessionContext session, ConversationTurn turn)
        {
            foreach (var (entityName, mention) in turn.Entities)
            {
                if (session.EntityTracker.TryGetValue(entityName, out var tracked))
                {
                    // Update existing entity
                    tracked.LastMention = turn.TurnId;
                    tracked.Boost(0.3f);
                }
                else
                {
                    // New entity
                    session.EntityTracker[entityName] = new TrackedEntity
                    {
                        Name = entityName,
                        Type = mention.Type,
                        FirstMention = turn.TurnId,
                        LastMention = turn.TurnId,
                        MentionCount = 1,
                        Salience = mention.Salience
                    };
                }
            }
            
            // Decay salience of entities not mentioned
            foreach (var (name, entity) in session.EntityTracker)
            {
                if (!turn.Entities.ContainsKey(name))
                {
                    entity.Decay(0.95f);
                }
            }
        }
    }
}
```

### Layer 2: User Context (Episodic Memory)

**Purpose**: Maintain long-term user profile and conversation history

**Graph Schema Extensions:**

```csharp
namespace Myriad.Core.Context.Graph
{
    /// <summary>
    /// User node in graph database
    /// </summary>
    public record UserNode : GraphNode
    {
        public required string UserId { get; init; }
        public DateTime CreatedAt { get; init; }
        public UserPreferences Preferences { get; init; } = new();
        public Dictionary<string, float> ExpertiseLevels { get; init; } = new();
        
        public UserNode() : base(NodeType.User) { }
    }
    
    /// <summary>
    /// Conversation node linking to turns
    /// </summary>
    public record ConversationNode : GraphNode
    {
        public required string ConversationId { get; init; }
        public required string SessionId { get; init; }
        public DateTime StartedAt { get; init; }
        public DateTime? EndedAt { get; init; }
        public required string Topic { get; init; }
        public string? Summary { get; init; }
        public ConversationStatus Status { get; init; }
        
        public ConversationNode() : base(NodeType.Conversation) { }
    }
    
    /// <summary>
    /// Turn node in conversation graph
    /// </summary>
    public record TurnNode : GraphNode
    {
        public required int TurnId { get; init; }
        public required string Query { get; init; }
        public string? ResolvedQuery { get; init; }
        public string? ResponseSummary { get; init; }
        public required string Intent { get; init; }
        public DateTime Timestamp { get; init; }
        
        public TurnNode() : base(NodeType.Turn) { }
    }
    
    public enum ConversationStatus
    {
        Active,
        Completed,
        Abandoned
    }
    
    public record UserPreferences
    {
        public string Verbosity { get; init; } = "moderate"; // brief, moderate, detailed
        public string Language { get; init; } = "en";
        public string ExplanationStyle { get; init; } = "technical"; // technical, analogies, examples
        public bool PreferClarification { get; init; } = true;
    }
}
```

**User Context Manager:**

```csharp
namespace Myriad.Core.Context
{
    /// <summary>
    /// Manages long-term user context in graph database
    /// </summary>
    public class UserContextManager
    {
        private readonly IGraphDatabase _graphDb;
        private readonly ILogger<UserContextManager> _logger;
        
        public UserContextManager(
            IGraphDatabase graphDb,
            ILogger<UserContextManager> logger)
        {
            _graphDb = graphDb;
            _logger = logger;
        }
        
        /// <summary>
        /// Create or get user profile
        /// </summary>
        public async Task<UserNode> GetOrCreateUserAsync(
            string userId,
            CancellationToken cancellationToken = default)
        {
            // Find existing user
            var users = await _graphDb.FindNodesAsync(
                n => n is UserNode un && un.UserId == userId,
                cancellationToken);
            
            var userNode = users.OfType<UserNode>().FirstOrDefault();
            
            if (userNode != null)
            {
                return userNode;
            }
            
            // Create new user
            var newUser = new UserNode
            {
                Id = Guid.NewGuid().ToString(),
                UserId = userId,
                CreatedAt = DateTime.UtcNow
            };
            
            await _graphDb.UpsertNodeAsync(newUser, cancellationToken);
            
            _logger.LogInformation("Created new user profile for {UserId}", userId);
            
            return newUser;
        }
        
        /// <summary>
        /// Create conversation in graph
        /// </summary>
        public async Task<string> CreateConversationAsync(
            string userId,
            string sessionId,
            string topic = "general",
            CancellationToken cancellationToken = default)
        {
            var conversationId = $"conv_{sessionId}";
            
            var conversation = new ConversationNode
            {
                Id = Guid.NewGuid().ToString(),
                ConversationId = conversationId,
                SessionId = sessionId,
                StartedAt = DateTime.UtcNow,
                Topic = topic,
                Status = ConversationStatus.Active
            };
            
            await _graphDb.UpsertNodeAsync(conversation, cancellationToken);
            
            // Link to user
            var userNode = await GetOrCreateUserAsync(userId, cancellationToken);
            var edge = new GraphEdge(userNode.Id, conversation.Id, EdgeType.StartedConversation);
            await _graphDb.AddEdgeAsync(edge, cancellationToken);
            
            return conversationId;
        }
        
        /// <summary>
        /// Add turn to conversation graph
        /// </summary>
        public async Task AddTurnToConversationAsync(
            string conversationId,
            ConversationTurn turn,
            CancellationToken cancellationToken = default)
        {
            var turnNode = new TurnNode
            {
                Id = Guid.NewGuid().ToString(),
                TurnId = turn.TurnId,
                Query = turn.Query,
                ResolvedQuery = turn.ResolvedQuery,
                ResponseSummary = turn.ResponseSummary,
                Intent = turn.Intent,
                Timestamp = turn.Timestamp
            };
            
            await _graphDb.UpsertNodeAsync(turnNode, cancellationToken);
            
            // Link to conversation
            var conversations = await _graphDb.FindNodesAsync(
                n => n is ConversationNode cn && cn.ConversationId == conversationId,
                cancellationToken);
            
            var conversationNode = conversations.OfType<ConversationNode>().FirstOrDefault();
            if (conversationNode != null)
            {
                var edge = new GraphEdge(conversationNode.Id, turnNode.Id, EdgeType.HasTurn)
                {
                    Properties = new Dictionary<string, object>
                    {
                        ["sequence"] = turn.TurnId
                    }
                };
                await _graphDb.AddEdgeAsync(edge, cancellationToken);
            }
            
            // Link to mentioned concepts
            foreach (var concept in turn.Concepts)
            {
                await LinkTurnToConceptAsync(turnNode.Id, concept, cancellationToken);
            }
        }
        
        /// <summary>
        /// Get user's conversation history
        /// </summary>
        public async Task<List<ConversationNode>> GetUserConversationsAsync(
            string userId,
            int limit = 10,
            CancellationToken cancellationToken = default)
        {
            // Query graph for user's conversations
            var conversations = await _graphDb.TraverseAsync(
                userId,
                n => n is ConversationNode,
                maxDepth: 2,
                cancellationToken);
            
            return conversations
                .OfType<ConversationNode>()
                .OrderByDescending(c => c.StartedAt)
                .Take(limit)
                .ToList();
        }
        
        private async Task LinkTurnToConceptAsync(
            string turnNodeId,
            string concept,
            CancellationToken cancellationToken)
        {
            var conceptNodes = await _graphDb.FindNodesAsync(
                n => n is ConceptNode cn && cn.Name.Equals(concept, StringComparison.OrdinalIgnoreCase),
                cancellationToken);
            
            var conceptNode = conceptNodes.OfType<ConceptNode>().FirstOrDefault();
            if (conceptNode != null)
            {
                var edge = new GraphEdge(turnNodeId, conceptNode.Id, EdgeType.Mentions);
                await _graphDb.AddEdgeAsync(edge, cancellationToken);
            }
        }
    }
}
```

### Layer 3: Reference Resolution Engine

**Purpose**: Resolve pronouns and references to entities

**C# Implementation:**

```csharp
namespace Myriad.Core.Context
{
    /// <summary>
    /// Resolves references (pronouns, demonstratives) to entities
    /// </summary>
    public class ReferenceResolver
    {
        private readonly ILogger<ReferenceResolver> _logger;
        
        // Pronoun patterns
        private static readonly Dictionary<string, string[]> PronounTypes = new()
        {
            ["singular_neutral"] = new[] { "it", "that", "this", "which" },
            ["singular_male"] = new[] { "he", "him", "his" },
            ["singular_female"] = new[] { "she", "her", "hers" },
            ["plural"] = new[] { "they", "them", "their", "these", "those" }
        };
        
        public ReferenceResolver(ILogger<ReferenceResolver> logger)
        {
            _logger = logger;
        }
        
        /// <summary>
        /// Resolve references in query using entity tracker
        /// </summary>
        public (string resolvedQuery, List<Resolution> resolutions) ResolveReferences(
            string query,
            ConcurrentDictionary<string, TrackedEntity> entityTracker)
        {
            var resolutions = new List<Resolution>();
            var resolvedQuery = query;
            
            // Find all pronouns in query
            var words = query.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            
            for (int i = 0; i < words.Length; i++)
            {
                var word = words[i].ToLowerInvariant().TrimEnd('.', ',', '?', '!');
                
                if (IsPronoun(word, out var pronounType))
                {
                    var resolution = ResolvePronoun(word, pronounType, entityTracker);
                    
                    if (resolution != null && resolution.Confidence > 0.7f)
                    {
                        resolutions.Add(resolution);
                        
                        // Replace pronoun with resolved entity
                        resolvedQuery = resolvedQuery.Replace(
                            words[i],
                            resolution.ResolvedTo,
                            StringComparison.OrdinalIgnoreCase);
                    }
                }
            }
            
            _logger.LogDebug(
                "Resolved {Count} references in query: '{Original}' → '{Resolved}'",
                resolutions.Count, query, resolvedQuery);
            
            return (resolvedQuery, resolutions);
        }
        
        /// <summary>
        /// Resolve a single pronoun to most likely entity
        /// </summary>
        private Resolution? ResolvePronoun(
            string pronoun,
            string pronounType,
            ConcurrentDictionary<string, TrackedEntity> entityTracker)
        {
            // Filter entities by type compatibility
            var candidates = entityTracker.Values
                .Where(e => IsCompatibleEntity(e.Type, pronounType))
                .OrderByDescending(e => e.Salience)
                .ThenByDescending(e => e.LastMention)
                .ToList();
            
            if (!candidates.Any())
            {
                return null;
            }
            
            var best = candidates.First();
            
            // Calculate confidence based on salience and recency
            var recencyBonus = candidates.Count > 1
                ? (best.LastMention - candidates[1].LastMention) * 0.1f
                : 0.2f;
            
            var confidence = Math.Min(1.0f, best.Salience + recencyBonus);
            
            return new Resolution
            {
                Original = pronoun,
                ResolvedTo = best.Name,
                Confidence = confidence,
                Method = ResolutionMethod.RuleBased,
                Reasoning = $"Most salient {best.Type} entity (salience: {best.Salience:F2})"
            };
        }
        
        /// <summary>
        /// Check if pronoun matches entity type
        /// </summary>
        private bool IsCompatibleEntity(string entityType, string pronounType)
        {
            return pronounType switch
            {
                "singular_neutral" => entityType != "Person",
                "singular_male" => entityType == "Person", // Would need gender tracking
                "singular_female" => entityType == "Person",
                "plural" => true, // Can refer to any type
                _ => false
            };
        }
        
        /// <summary>
        /// Check if word is a pronoun
        /// </summary>
        private bool IsPronoun(string word, out string pronounType)
        {
            foreach (var (type, pronouns) in PronounTypes)
            {
                if (pronouns.Contains(word))
                {
                    pronounType = type;
                    return true;
                }
            }
            
            pronounType = string.Empty;
            return false;
        }
    }
    
    public record Resolution
    {
        public required string Original { get; init; }
        public required string ResolvedTo { get; init; }
        public required float Confidence { get; init; }
        public required ResolutionMethod Method { get; init; }
        public required string Reasoning { get; init; }
    }
    
    public enum ResolutionMethod
    {
        RuleBased,
        LlmPowered,
        Hybrid
    }
}
```

---

## Implementation Approaches

### Approach 1: In-Memory Session Management (Recommended for Phase 1)

**Using `MemoryCache`** (built-in to .NET):

```csharp
// Program.cs
builder.Services.AddMemoryCache();
builder.Services.AddSingleton<SessionContextManager>();
```

**Advantages:**

- ✅ Zero external dependencies
- ✅ Built into .NET
- ✅ Fast access (nanoseconds)
- ✅ Automatic expiration

**Disadvantages:**

- ❌ Single-server only (no distribution)
- ❌ Lost on restart

### Approach 2: Redis-Based Session Management (Recommended for Production)

**For distributed scenarios:**

```csharp
// Using StackExchange.Redis (optional external dependency)
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = configuration["Redis:ConnectionString"];
    options.InstanceName = "MyriadSessions:";
});
```

**Advantages:**

- ✅ Distributed across servers
- ✅ Survives restarts
- ✅ Sub-millisecond access
- ✅ Built-in TTL

**Disadvantages:**

- ❌ External dependency
- ❌ Additional infrastructure

### Approach 3: LLM-Enhanced Reference Resolution (Optional)

**For advanced cases:**

```csharp
public class LlmReferenceResolver
{
    private readonly HttpClient _httpClient;
    private readonly ReferenceResolver _fallback;
    
    public async Task<string> ResolveWithLlmAsync(
        string query,
        List<ConversationTurn> history,
        CancellationToken cancellationToken)
    {
        try
        {
            var prompt = BuildResolutionPrompt(query, history);
            var response = await CallLlmAsync(prompt, cancellationToken);
            return response;
        }
        catch
        {
            // Fallback to rule-based
            return _fallback.ResolveReferences(query, entityTracker).resolvedQuery;
        }
    }
}
```

---

## Integration with Existing Components

### Enhanced Input Processor Integration

**Modifications to existing [`InputProcessor`](../src/Myriad.Services.InputProcessor/InputProcessor.cs):**

```csharp
public class ContextAwareInputProcessor
{
    private readonly SessionContextManager _sessionContext;
    private readonly UserContextManager _userContext;
    private readonly ReferenceResolver _referenceResolver;
    
    public async Task<TaskList> ProcessQueryWithContextAsync(
        string rawQuery,
        string userId,
        string? sessionId = null,
        CancellationToken cancellationToken = default)
    {
        // Step 1: Get or create session
        var session = _sessionContext.GetOrCreateSession(userId, sessionId);
        
        // Step 2: Get recent context
        var recentTurns = _sessionContext.GetRecentContext(session.SessionId, 3);
        var entityTracker = _sessionContext.GetEntityTracker(session.SessionId);
        
        // Step 3: Resolve references
        var (resolvedQuery, resolutions) = _referenceResolver.ResolveReferences(
            rawQuery,
            entityTracker);
        
        // Step 4: Build enriched context
        var enrichedContext = new Dictionary<string, object>
        {
            ["session_id"] = session.SessionId,
            ["user_id"] = userId,
            ["previous_queries"] = recentTurns.Select(t => t.Query).ToList(),
            ["entity_tracker"] = entityTracker,
            ["active_topics"] = session.ActiveTopics,
            ["resolutions"] = resolutions
        };
        
        // Step 5: Process with original pipeline (now context-aware)
        var taskList = await ProcessQueryAsync(resolvedQuery, enrichedContext, cancellationToken);
        
        // Step 6: Store turn in session
        var turn = new ConversationTurn
        {
            TurnId = recentTurns.Count + 1,
            Query = rawQuery,
            ResolvedQuery = resolvedQuery,
            Concepts = ExtractConcepts(resolvedQuery),
            Entities = ExtractEntities(resolvedQuery, entityTracker),
            Intent = taskList.PrimaryIntent
        };
        
        _sessionContext.AddTurn(session.SessionId, turn);
        
        // Step 7: Persist to graph (async, non-blocking)
        _ = Task.Run(async () =>
        {
            if (recentTurns.Count == 0)
            {
                await _userContext.CreateConversationAsync(
                    userId,
                    session.SessionId,
                    cancellationToken: CancellationToken.None);
            }
            
            await _userContext.AddTurnToConversationAsync(
                $"conv_{session.SessionId}",
                turn,
                CancellationToken.None);
        });
        
        return taskList;
    }
}
```

### Context-Aware Agent Selection

**Enhancement to [`EnhancedGraphIntelligence`](graph-intelligence-csharp.md):**

```csharp
public async Task<List<AgentRelevanceScore>> DiscoverAgentsWithContextAsync(
    string concept,
    string intent,
    SessionContext sessionContext,
    CancellationToken cancellationToken)
{
    // Standard discovery
    var baseAgents = await DiscoverAgentsAsync(concept, intent, null, cancellationToken);
    
    // Boost agents recently used in conversation
    var recentAgentIds = sessionContext.TurnHistory
        .SelectMany(t => t.Concepts)
        .Distinct()
        .ToHashSet();
    
    foreach (var agent in baseAgents)
    {
        if (recentAgentIds.Contains(agent.AgentId))
        {
            agent.RelevanceScore = Math.Min(1.0f, agent.RelevanceScore * 1.2f);
            agent.Reasoning.Add("Recently used in conversation");
        }
    }
    
    return baseAgents.OrderByDescending(a => a.RelevanceScore).ToList();
}
```

---

## Implementation Roadmap

### Phase 1: Basic Session Context (Week 1-2)

**Goal**: Enable conversation memory within a session

**Tasks:**

1. ✅ Implement `SessionContext` data model
2. ✅ Implement `SessionContextManager` with `MemoryCache`
3. ✅ Add turn history tracking (last 10 turns)
4. ✅ Implement entity tracking with salience
5. ✅ Create basic reference resolution
6. ✅ Integrate with Input Processor
7. ✅ Add session ID to API

**Deliverable**: System resolves "Who invented it?" after "What is a lightbulb?"

**Acceptance Criteria:**

- Session context persists for 30 minutes
- Pronouns resolved using entity tracker
- Turn history maintained in sliding window
- Entity salience decays appropriately

### Phase 2: Graph-Based Persistence (Week 3-4)

**Goal**: Store conversation history for long-term learning

**Tasks:**

1. ✅ Extend graph schema with User, Conversation, Turn nodes
2. ✅ Implement `UserContextManager`
3. ✅ Create user-conversation relationships
4. ✅ Link turns to concepts via edges
5. ✅ Implement conversation flow tracking
6. ✅ Add user preference storage
7. ✅ Integrate with context-aware agent selection

**Deliverable**: System learns from past conversations

### Phase 3: Advanced Features (Week 5-8)

**Goal**: Add sophisticated context understanding

**Tasks:**

1. ⚠️ Optional: Integrate LLM for complex references
2. ✅ Implement topic transition detection
3. ✅ Add conversation summarization
4. ✅ Create user expertise tracking
5. ✅ Implement adaptive explanation depth

**Deliverable**: Human-like context understanding

---

## Example Scenarios

### Scenario 1: Basic Reference Resolution

```csharp
// Turn 1
User: "What is a lightbulb?"
System: "A lightbulb is a device that produces light..."

[Session Context Updated]
- entity_tracker: {"lightbulb": {salience: 0.9, type: "Concept"}}
- turn_history: [Turn 1]

// Turn 2
User: "Who invented it?"

[Reference Resolution]
- Detected pronoun: "it"
- Entity candidates: ["lightbulb" (salience: 0.9)]
- Resolution: "it" → "lightbulb" (confidence: 0.95)
- Resolved query: "Who invented the lightbulb?"

System: ✅ "Thomas Edison invented the lightbulb in 1879..."

[Session Context Updated]
- entity_tracker: {
    "lightbulb": {salience: 0.85, mention_count: 2},
    "Thomas Edison": {salience: 0.9, type: "Person"}
  }
```

### Scenario 2: Multi-Turn Topic Continuity

```csharp
// Turn 1
User: "Explain quantum mechanics"
System: [Detailed explanation]

[Context] topic="quantum_physics", expertise_level="unknown"

// Turn 2
User: "That's too complex"

[Context Update] expertise_level="beginner", verbosity="simple"

// Turn 3
User: "Can you simplify?"
System: ✅ [Simpler explanation with analogies]

[Context Update] prefers_analogies=true

// Later conversation
User: "Explain relativity"

[Context Applied]
- Retrieved user preferences: expertise="beginner", prefers_analogies=true
- Automatically provides simple explanation with analogies
System: ✅ "Think of relativity like being on a moving train..."
```

### Scenario 3: Context-Aware Agent Selection

```csharp
// Turn 1
User: "What is machine learning?"
[Selected: ML_Definition_Agent]
[Recorded: successful agent usage]

// Turn 2
User: "How do neural networks learn?"

[Context-Aware Selection]
- Recent conversation: machine learning
- Collaboration pattern: ML_Definition_Agent + Neural_Network_Agent
- Domain continuity: both in AI domain
- User mode: learning (progressive explanation)

[Selected: Neural_Network_Agent WITH collaboration hint]

System: ✅ "Building on what we discussed about machine learning, 
           neural networks learn by adjusting connection weights..."
```

---

## Performance Considerations

### Target Metrics

| Operation | Target | Max Acceptable |
|-----------|--------|----------------|
| Session retrieval | < 5ms | < 20ms |
| Entity update | < 10ms | < 50ms |
| Reference resolution (rule) | < 50ms | < 100ms |
| Graph persistence | < 100ms | < 300ms |
| Full context enrichment | < 200ms | < 500ms |

### Optimization Strategies

1. **Session Caching**: Keep active sessions in memory
2. **Lazy Graph Persistence**: Async write to graph database
3. **Entity Tracker Pruning**: Remove low-salience entities periodically
4. **Reference Resolution Cache**: Cache common pronoun resolutions
5. **Batch Graph Updates**: Aggregate multiple turn updates

### Scalability

| Metric | Phase 1 | Phase 2 | Production |
|--------|---------|---------|------------|
| Concurrent sessions | 100 | 1,000 | 10,000 |
| Active users | 500 | 5,000 | 50,000 |
| Memory per session | ~100KB | ~500KB | ~1MB |
| Storage per user | - | 1MB | 10MB |

---

**Document Version:** 1.0 C#  
**Last Updated:** 2025-01-10  
**Status:** Architecture Definition Phase

[↑ Back to Index](../INDEX.md) | [Graph Intelligence ←](graph-intelligence-csharp.md) | [Microservices →](microservices-csharp.md)
