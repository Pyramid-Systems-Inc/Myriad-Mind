# Myriad Cognitive Architecture - Cognitive Synthesizer Design (C#/.NET Edition)

**Architecture Documentation** | [Overview](system-overview-csharp.md) | [Microservices](microservices-csharp.md) | [Production](production-deployment-csharp.md)

Comprehensive design for transforming raw agent data into human-like, well-organized explanations through a four-stage synthesis pipeline - all built in C# without external NLP dependencies.

[← Back to Index](../INDEX.md#architecture) | [Microservices ←](microservices-csharp.md)

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [The Human Analogy](#the-human-analogy)
- [Current System Analysis](#current-system-analysis)
- [Four-Stage Synthesis Pipeline](#four-stage-synthesis-pipeline)
- [Component Implementation](#component-implementation)
- [Integration Architecture](#integration-architecture)
- [Example Transformations](#example-transformations)
- [Implementation Roadmap](#implementation-roadmap)
- [Performance Considerations](#performance-considerations)

---

## Executive Summary

### Relationship to Cognitive Workspace

This document describes the **Cognitive Synthesizer**, which operates within the Output Processor to transform agent responses into human-like narratives. This is distinct from but complementary to the **Cognitive Workspace**:

- **Cognitive Workspace**: Handles deep reasoning for complex queries (pattern recognition, causal analysis, simulation)
- **Cognitive Synthesizer**: Transforms any set of agent responses (from either processing path) into well-structured, coherent narratives

Both work together to provide high-quality responses: the Workspace enables deep thinking, while the Synthesizer ensures effective communication.

### The Challenge

The current Output Processor excels at **aggregating facts** from specialized agents but lacks the ability to **weave them into coherent narratives** that mimic human explanation. Users receive disconnected facts rather than well-structured, extensive answers.

**Current Limitation:**

```
"A lightbulb is an electric device. The lightbulb extended working hours. 
Factories became more productive. Worker safety improved."
```

**Target Output:**

```
Summary: The lightbulb was a cornerstone of the industrial revolution, 
primarily because it enabled factories to operate safely and efficiently 
around the clock.

To fully appreciate its importance, consider the historical context...
[Detailed, flowing narrative with transitions]

Related Topics: Thomas Edison, Industrial Revolution, Factory Labor
```

### Proposed Solution

Implement a **Four-Stage Cognitive Synthesizer** that transforms aggregated data through specialized micro-agents. This works for responses from both the Fast Path (simple retrieval) and Deep Reasoning Path (Cognitive Workspace):

1. **Stage 1: Thematic Analyzer** - Groups raw facts into logical themes
2. **Stage 2: Narrative Weaver** - Constructs coherent narrative with transitions
3. **Stage 3: Summarizer & Expander** - Creates layered response with related topics
4. **Stage 4: Final Formatter** - Polishes output with confidence-modulated language

### Processing Flow Integration

```
Fast Path Query → Agent Responses → Cognitive Synthesizer → Formatted Output
Deep Reasoning Path → Cognitive Workspace → Synthesis Results → Cognitive Synthesizer → Formatted Output
```

### Key Benefits

- ✅ **Human-Like Output**: Structured, extensive, easy to understand
- ✅ **Emergent Synthesis**: Collaborative agent-based approach
- ✅ **Layered Information**: Summary + details + related topics
- ✅ **Transparent & Modular**: Explainable synthesis process
- ✅ **Zero External Dependencies**: Custom C# implementation

---

## The Human Analogy

### How Humans Construct Explanations

When a human expert answers a complex question, they perform these cognitive steps:

#### 1. Organize Thoughts

Group available information into themes:

- Historical context
- Technical details
- Impacts and consequences
- Future implications

#### 2. Construct Narrative

Build logical flow:

- Start with key concept
- Provide supporting evidence
- Use transitions ("Therefore," "However," "Furthermore")
- Build toward conclusion

#### 3. Consider Audience

Adapt presentation:

- Provide executive summary
- Adjust detail level
- Anticipate follow-up questions
- Suggest related topics

#### 4. Express Confidence

Modulate language:

- High certainty: "It is certain that..."
- Medium: "The evidence suggests..."
- Low: "It appears that..."

### Myriad's Agent-Based Approach

```
┌─────────────────────────────────────────────────────────────┐
│              Human Cognitive Process                         │
├─────────────────────────────────────────────────────────────┤
│  Organize → Narrate → Layer → Express                       │
│  Thoughts   Story    Info     Confidence                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
                     Mapped to
                           ↓
┌─────────────────────────────────────────────────────────────┐
│         Myriad Cognitive Synthesizer Pipeline                │
├─────────────────────────────────────────────────────────────┤
│  Stage 1  →  Stage 2  →  Stage 3   →  Stage 4              │
│  Thematic    Narrative   Summarizer   Formatter             │
│  Analyzer    Weaver      Expander     (Confidence)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Current System Analysis

### Existing Output Processor

**Location**: `src/Myriad.Services.OutputProcessor/`

**Current Architecture:**

```csharp
public class OutputProcessorService
{
    private readonly IResponseSynthesizer _synthesizer;
    private readonly IResponseFormatter _formatter;
    
    public async Task<FormattedResponse> ProcessResponseAsync(
        List<AgentResponse> agentResponses,
        string originalQuery,
        CancellationToken cancellationToken)
    {
        // Step 1: Simple aggregation
        var synthesized = await _synthesizer.SynthesizeAsync(
            agentResponses,
            cancellationToken);
        
        // Step 2: Basic formatting
        var formatted = await _formatter.FormatAsync(
            synthesized,
            ResponseFormat.Explanatory,
            cancellationToken);
        
        return formatted;
    }
}
```

### Current Limitations

| Aspect | Current Behavior | Desired Behavior |
|--------|------------------|------------------|
| **Structure** | Flat aggregation | Thematic organization |
| **Flow** | Disconnected facts | Coherent narrative |
| **Layering** | Single text block | Summary + details |
| **Guidance** | No suggestions | Related topics |
| **Confidence** | Fixed language | Modulated by certainty |

**Example Current Output:**

```
A lightbulb is an electric device that produces light. The lightbulb 
revolutionized factory work. It extended productive hours. It improved 
worker safety. It enabled 24-hour operations.

Sources: Lightbulb_Definition_AI, Factory_History_AI
```

**Problems:**

- ❌ No thematic grouping (definition vs impact)
- ❌ Choppy, repetitive sentences
- ❌ No introduction or conclusion
- ❌ No summary for quick understanding
- ❌ Missing related topics

---

## Four-Stage Synthesis Pipeline

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         Collected Results (from Fast Path OR                 │
│         Cognitive Workspace Deep Reasoning)                  │
│  {                                                           │
│    "task_1": {"data": "Lightbulb definition..."},           │
│    "task_2": {"data": "Factory history..."},                │
│    "task_3": {"data": "Safety improvements..."}             │
│  }                                                           │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Thematic Analyzer AI                              │
│  - Clusters facts by semantic similarity                    │
│  - Creates structured content plan                          │
│  - Output: { "intro": [...], "themes": {...} }             │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Narrative Weaver AI                               │
│  - Constructs flowing paragraphs                            │
│  - Injects transition words                                 │
│  - Synthesizes related points                               │
│  - Output: "Coherent draft text..."                         │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: Summarizer & Expander AI                          │
│  - Generates executive summary                              │
│  - Extracts key concepts                                    │
│  - Suggests related topics                                  │
│  - Output: { summary, details, related_topics }            │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 4: Final Formatter                                   │
│  - Applies confidence-modulated language                    │
│  - Formats with Markdown                                    │
│  - Adds source attribution                                  │
│  - Output: Final polished response                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Implementation

### Stage 1: Thematic Analyzer AI

**Type**: Pattern-Matcher Agent (Type C)  
**Location**: `src/Myriad.Agents.Synthesis/ThematicAnalyzer/`

**C# Implementation:**

```csharp
namespace Myriad.Agents.Synthesis.ThematicAnalyzer
{
    /// <summary>
    /// Analyzes and groups facts into logical themes
    /// </summary>
    public class ThematicAnalyzerAgent
    {
        private readonly ILogger<ThematicAnalyzerAgent> _logger;
        
        /// <summary>
        /// Analyze collected results and create content plan
        /// </summary>
        public async Task<ContentPlan> AnalyzeThemesAsync(
            Dictionary<string, AgentResult> collectedResults,
            CancellationToken cancellationToken = default)
        {
            // Extract all text segments
            var segments = ExtractTextSegments(collectedResults);
            
            // Compute semantic clusters (custom implementation)
            var clusters = await ClusterBySemanticSimilarityAsync(segments, cancellationToken);
            
            // Assign thematic labels
            var themes = AssignThematicLabels(clusters);
            
            // Build content plan
            var plan = new ContentPlan
            {
                Introduction = IdentifyIntroductoryContent(themes),
                Themes = themes,
                Conclusion = IdentifyClosingContent(themes)
            };
            
            _logger.LogInformation(
                "Created content plan with {ThemeCount} themes",
                themes.Count);
            
            return plan;
        }
        
        /// <summary>
        /// Extract text segments from agent results
        /// </summary>
        private List<TextSegment> ExtractTextSegments(
            Dictionary<string, AgentResult> results)
        {
            var segments = new List<TextSegment>();
            
            foreach (var (taskId, result) in results)
            {
                if (result.Data.TryGetValue("text", out var textObj) &&
                    textObj is string text)
                {
                    segments.Add(new TextSegment
                    {
                        Id = taskId,
                        Text = text,
                        Source = result.AgentId
                    });
                }
            }
            
            return segments;
        }
        
        /// <summary>
        /// Cluster segments by semantic similarity (custom algorithm)
        /// </summary>
        private async Task<List<Cluster>> ClusterBySemanticSimilarityAsync(
            List<TextSegment> segments,
            CancellationToken cancellationToken)
        {
            // Simple keyword-based clustering (no external NLP)
            var clusters = new List<Cluster>();
            var keywordMap = new Dictionary<string, List<TextSegment>>();
            
            // Define theme keywords
            var themeKeywords = new Dictionary<string, string[]>
            {
                ["Historical"] = new[] { "history", "invented", "created", "era", "century" },
                ["Technical"] = new[] { "works", "mechanism", "technical", "process", "function" },
                ["Impact"] = new[] { "impact", "effect", "influence", "changed", "revolutionized" },
                ["Safety"] = new[] { "safety", "hazard", "risk", "protection", "secure" }
            };
            
            foreach (var segment in segments)
            {
                var textLower = segment.Text.ToLowerInvariant();
                var matchedThemes = new List<string>();
                
                foreach (var (theme, keywords) in themeKeywords)
                {
                    if (keywords.Any(kw => textLower.Contains(kw)))
                    {
                        matchedThemes.Add(theme);
                    }
                }
                
                // Assign to best matching theme or "General"
                var primaryTheme = matchedThemes.FirstOrDefault() ?? "General";
                
                if (!keywordMap.ContainsKey(primaryTheme))
                {
                    keywordMap[primaryTheme] = new List<TextSegment>();
                }
                
                keywordMap[primaryTheme].Add(segment);
            }
            
            // Convert to clusters
            foreach (var (theme, segs) in keywordMap)
            {
                clusters.Add(new Cluster
                {
                    Theme = theme,
                    Segments = segs
                });
            }
            
            return clusters;
        }
        
        /// <summary>
        /// Assign thematic labels to clusters
        /// </summary>
        private Dictionary<string, List<string>> AssignThematicLabels(
            List<Cluster> clusters)
        {
            var themes = new Dictionary<string, List<string>>();
            
            foreach (var cluster in clusters)
            {
                themes[cluster.Theme] = cluster.Segments
                    .Select(s => s.Id)
                    .ToList();
            }
            
            return themes;
        }
        
        private List<string> IdentifyIntroductoryContent(
            Dictionary<string, List<string>> themes)
        {
            // Find general/definition content for introduction
            if (themes.TryGetValue("General", out var general))
            {
                return general.Take(2).ToList();
            }
            
            return new List<string>();
        }
        
        private List<string> IdentifyClosingContent(
            Dictionary<string, List<string>> themes)
        {
            // Find impact/conclusion content
            if (themes.TryGetValue("Impact", out var impact))
            {
                return impact.TakeLast(1).ToList();
            }
            
            return new List<string>();
        }
    }
    
    public record ContentPlan
    {
        public List<string> Introduction { get; init; } = new();
        public Dictionary<string, List<string>> Themes { get; init; } = new();
        public List<string> Conclusion { get; init; } = new();
    }
    
    public record TextSegment
    {
        public required string Id { get; init; }
        public required string Text { get; init; }
        public required string Source { get; init; }
    }
    
    public record Cluster
    {
        public required string Theme { get; init; }
        public required List<TextSegment> Segments { get; init; }
    }
}
```

**ASP.NET Core Endpoint:**

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapPost("/analyze_themes", async (
    ThemeAnalysisRequest request,
    ThematicAnalyzerAgent analyzer,
    CancellationToken cancellationToken) =>
{
    var plan = await analyzer.AnalyzeThemesAsync(
        request.CollectedResults,
        cancellationToken);
    
    return Results.Ok(plan);
});

app.Run();

record ThemeAnalysisRequest(
    Dictionary<string, AgentResult> CollectedResults);
```

### Stage 2: Narrative Weaver AI

**Type**: Micro-Generator Agent (Type D)  
**Location**: `src/Myriad.Agents.Synthesis/NarrativeWeaver/`

**C# Implementation:**

```csharp
namespace Myriad.Agents.Synthesis.NarrativeWeaver
{
    /// <summary>
    /// Weaves facts into coherent narrative with transitions
    /// </summary>
    public class NarrativeWeaverAgent
    {
        private readonly ILogger<NarrativeWeaverAgent> _logger;
        
        // Transition phrases for narrative flow
        private static readonly Dictionary<string, string[]> Transitions = new()
        {
            ["continuation"] = new[] { "Furthermore,", "Additionally,", "Moreover," },
            ["causation"] = new[] { "Therefore,", "As a result,", "Consequently," },
            ["contrast"] = new[] { "However,", "On the other hand,", "Nevertheless," },
            ["elaboration"] = new[] { "To elaborate,", "More specifically,", "In detail," }
        };
        
        /// <summary>
        /// Weave content plan into coherent narrative
        /// </summary>
        public async Task<CoherentDraft> WeaveNarrativeAsync(
            ContentPlan plan,
            Dictionary<string, AgentResult> originalResults,
            CancellationToken cancellationToken = default)
        {
            var paragraphs = new List<string>();
            
            // Build introduction
            if (plan.Introduction.Any())
            {
                var intro = BuildIntroduction(plan.Introduction, originalResults);
                paragraphs.Add(intro);
            }
            
            // Build themed paragraphs
            foreach (var (theme, segmentIds) in plan.Themes)
            {
                var paragraph = BuildThemedParagraph(
                    theme,
                    segmentIds,
                    originalResults);
                
                paragraphs.Add(paragraph);
            }
            
            // Build conclusion
            if (plan.Conclusion.Any())
            {
                var conclusion = BuildConclusion(plan.Conclusion, originalResults);
                paragraphs.Add(conclusion);
            }
            
            // Join with proper spacing
            var narrative = string.Join("\n\n", paragraphs);
            
            return new CoherentDraft
            {
                Text = narrative,
                ParagraphCount = paragraphs.Count
            };
        }
        
        /// <summary>
        /// Build introduction paragraph
        /// </summary>
        private string BuildIntroduction(
            List<string> segmentIds,
            Dictionary<string, AgentResult> results)
        {
            var sentences = segmentIds
                .Select(id => ExtractText(id, results))
                .Where(t => !string.IsNullOrEmpty(t))
                .ToList();
            
            if (!sentences.Any())
            {
                return "";
            }
            
            // Start with context phrase
            return $"To understand this fully, it's helpful to start with the basics. {string.Join(" ", sentences)}";
        }
        
        /// <summary>
        /// Build themed paragraph with transitions
        /// </summary>
        private string BuildThemedParagraph(
            string theme,
            List<string> segmentIds,
            Dictionary<string, AgentResult> results)
        {
            var sentences = segmentIds
                .Select(id => ExtractText(id, results))
                .Where(t => !string.IsNullOrEmpty(t))
                .ToList();
            
            if (!sentences.Any())
            {
                return "";
            }
            
            var paragraph = new StringBuilder();
            
            // Theme introduction
            paragraph.Append(GetThemeIntroduction(theme));
            paragraph.Append(" ");
            
            // First sentence
            paragraph.Append(sentences[0]);
            
            // Subsequent sentences with transitions
            for (int i = 1; i < sentences.Count; i++)
            {
                var transitionType = DetermineTransitionType(
                    sentences[i - 1],
                    sentences[i]);
                
                paragraph.Append(" ");
                paragraph.Append(GetTransition(transitionType));
                paragraph.Append(" ");
                paragraph.Append(sentences[i]);
            }
            
            return paragraph.ToString();
        }
        
        /// <summary>
        /// Build conclusion paragraph
        /// </summary>
        private string BuildConclusion(
            List<string> segmentIds,
            Dictionary<string, AgentResult> results)
        {
            var sentences = segmentIds
                .Select(id => ExtractText(id, results))
                .Where(t => !string.IsNullOrEmpty(t))
                .ToList();
            
            if (!sentences.Any())
            {
                return "";
            }
            
            return $"In summary, {string.Join(" ", sentences)}";
        }
        
        /// <summary>
        /// Determine appropriate transition between sentences
        /// </summary>
        private string DetermineTransitionType(string sentence1, string sentence2)
        {
            var s1Lower = sentence1.ToLowerInvariant();
            var s2Lower = sentence2.ToLowerInvariant();
            
            // Check for contrast
            if (s1Lower.Contains("not") || s1Lower.Contains("no") ||
                s2Lower.Contains("however") || s2Lower.Contains("but"))
            {
                return "contrast";
            }
            
            // Check for causation
            if (s2Lower.Contains("result") || s2Lower.Contains("therefore") ||
                s2Lower.Contains("because"))
            {
                return "causation";
            }
            
            // Check for elaboration
            if (s2Lower.Contains("specifically") || s2Lower.Contains("detail"))
            {
                return "elaboration";
            }
            
            // Default to continuation
            return "continuation";
        }
        
        /// <summary>
        /// Get random transition phrase for type
        /// </summary>
        private string GetTransition(string type)
        {
            if (Transitions.TryGetValue(type, out var phrases))
            {
                var random = new Random();
                return phrases[random.Next(phrases.Length)];
            }
            
            return "Additionally,";
        }
        
        private string GetThemeIntroduction(string theme)
        {
            return theme switch
            {
                "Historical" => "Looking at the historical context,",
                "Technical" => "From a technical perspective,",
                "Impact" => "Regarding its impact,",
                "Safety" => "In terms of safety,",
                _ => "Furthermore,"
            };
        }
        
        private string? ExtractText(string id, Dictionary<string, AgentResult> results)
        {
            if (results.TryGetValue(id, out var result) &&
                result.Data.TryGetValue("text", out var textObj))
            {
                return textObj.ToString();
            }
            
            return null;
        }
    }
    
    public record CoherentDraft
    {
        public required string Text { get; init; }
        public int ParagraphCount { get; init; }
    }
}
```

### Stage 3: Summarizer & Expander AI

**Type**: Micro-Generator Agent (Type D)  
**Location**: `src/Myriad.Agents.Synthesis/SummarizerExpander/`

**C# Implementation:**

```csharp
namespace Myriad.Agents.Synthesis.SummarizerExpander
{
    /// <summary>
    /// Creates layered response with summary and related topics
    /// </summary>
    public class SummarizerExpanderAgent
    {
        private readonly IGraphDatabase _graphDb;
        private readonly ILogger<SummarizerExpanderAgent> _logger;
        
        public SummarizerExpanderAgent(
            IGraphDatabase graphDb,
            ILogger<SummarizerExpanderAgent> logger)
        {
            _graphDb = graphDb;
            _logger = logger;
        }
        
        /// <summary>
        /// Create layered response from coherent draft
        /// </summary>
        public async Task<LayeredResponse> CreateLayeredResponseAsync(
            CoherentDraft draft,
            float confidence,
            List<string> sources,
            CancellationToken cancellationToken = default)
        {
            // Generate summary
            var summary = GenerateSummary(draft.Text);
            
            // Extract key concepts
            var keyConcepts = ExtractKeyConcepts(draft.Text);
            
            // Find related topics
            var relatedTopics = await FindRelatedTopicsAsync(
                keyConcepts,
                cancellationToken);
            
            return new LayeredResponse
            {
                Summary = summary,
                Details = draft.Text,
                Confidence = confidence,
                Sources = sources,
                RelatedTopics = relatedTopics
            };
        }
        
        /// <summary>
        /// Generate executive summary (1-2 sentences)
        /// </summary>
        private string GenerateSummary(string fullText)
        {
            // Find first few sentences
            var sentences = SplitIntoSentences(fullText);
            
            if (sentences.Count == 0)
            {
                return "No summary available.";
            }
            
            // Take first sentence or first two if very short
            if (sentences[0].Length < 100 && sentences.Count > 1)
            {
                return $"{sentences[0]} {sentences[1]}";
            }
            
            return sentences[0];
        }
        
        /// <summary>
        /// Extract key concepts from text
        /// </summary>
        private List<string> ExtractKeyConcepts(string text)
        {
            // Simple approach: Extract capitalized phrases and important nouns
            var words = text.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            var concepts = new HashSet<string>();
            
            for (int i = 0; i < words.Length; i++)
            {
                var word = words[i].Trim('.', ',', '!', '?', ';', ':');
                
                // Check for capitalized words (potential proper nouns)
                if (char.IsUpper(word[0]) && word.Length > 3)
                {
                    // Check for multi-word concepts
                    if (i + 1 < words.Length && char.IsUpper(words[i + 1][0]))
                    {
                        var multiWord = $"{word} {words[i + 1].Trim('.', ',', '!', '?')}";
                        concepts.Add(multiWord);
                    }
                    else
                    {
                        concepts.Add(word);
                    }
                }
            }
            
            return concepts.Take(5).ToList();
        }
        
        /// <summary>
        /// Find related topics from graph database
        /// </summary>
        private async Task<List<string>> FindRelatedTopicsAsync(
            List<string> keyConcepts,
            CancellationToken cancellationToken)
        {
            var relatedTopics = new HashSet<string>();
            
            foreach (var concept in keyConcepts)
            {
                // Find related concepts in graph
                var conceptNodes = await _graphDb.FindNodesAsync(
                    n => n is ConceptNode cn && 
                         cn.Name.Contains(concept, StringComparison.OrdinalIgnoreCase),
                    cancellationToken);
                
                var conceptNode = conceptNodes.OfType<ConceptNode>().FirstOrDefault();
                
                if (conceptNode != null)
                {
                    // Traverse to related concepts
                    var related = await _graphDb.TraverseAsync(
                        conceptNode.Id,
                        n => n is ConceptNode,
                        maxDepth: 2,
                        cancellationToken);
                    
                    foreach (var node in related.OfType<ConceptNode>().Take(3))
                    {
                        if (node.Name != concept)
                        {
                            relatedTopics.Add(node.Name);
                        }
                    }
                }
            }
            
            return relatedTopics.Take(5).ToList();
        }
        
        private List<string> SplitIntoSentences(string text)
        {
            // Simple sentence splitter
            return text
                .Split(new[] { ". ", "! ", "? " }, StringSplitOptions.RemoveEmptyEntries)
                .Select(s => s.Trim())
                .Where(s => !string.IsNullOrEmpty(s))
                .ToList();
        }
    }
    
    public record LayeredResponse
    {
        public required string Summary { get; init; }
        public required string Details { get; init; }
        public required float Confidence { get; init; }
        public required List<string> Sources { get; init; }
        public required List<string> RelatedTopics { get; init; }
    }
}
```

### Stage 4: Final Formatter with Confidence Modulation

**Enhanced Formatter:**

```csharp
namespace Myriad.Services.OutputProcessor
{
    /// <summary>
    /// Final formatter with confidence-modulated language
    /// </summary>
    public class CognitiveFormatter
    {
        private readonly ILogger<CognitiveFormatter> _logger;
        
        /// <summary>
        /// Format layered response with confidence modulation
        /// </summary>
        public string FormatResponse(LayeredResponse response)
        {
            var output = new StringBuilder();
            
            // Add confidence-modulated summary
            output.AppendLine("## Summary");
            output.AppendLine();
            output.Append(GetConfidencePrefix(response.Confidence));
            output.Append(" ");
            output.AppendLine(response.Summary);
            output.AppendLine();
            
            // Add detailed explanation
            output.AppendLine("## Detailed Explanation");
            output.AppendLine();
            output.AppendLine(response.Details);
            output.AppendLine();
            
            // Add related topics if available
            if (response.RelatedTopics.Any())
            {
                output.AppendLine("## Related Topics You Might Be Interested In");
                output.AppendLine();
                
                foreach (var topic in response.RelatedTopics)
                {
                    output.AppendLine($"- {topic}");
                }
                
                output.AppendLine();
            }
            
            // Add source attribution
            output.AppendLine("## Sources");
            output.AppendLine();
            output.AppendLine(string.Join(", ", response.Sources));
            
            return output.ToString();
        }
        
        /// <summary>
        /// Get confidence-modulated prefix phrase
        /// </summary>
        private string GetConfidencePrefix(float confidence)
        {
            return confidence switch
            {
                >= 0.9f => "It is certain that",
                >= 0.8f => "The evidence strongly suggests that",
                >= 0.7f => "The analysis indicates that",
                >= 0.6f => "It appears that",
                >= 0.5f => "Available information suggests that",
                _ => "Based on limited data, it seems that"
            };
        }
    }
}
```

---

## Integration Architecture

### Enhanced Output Processor

**Complete Pipeline Implementation:**

```csharp
namespace Myriad.Services.OutputProcessor
{
    /// <summary>
    /// Enhanced output processor with four-stage synthesis
    /// </summary>
    public class CognitiveSynthesisProcessor
    {
        private readonly HttpClient _httpClient;
        private readonly CognitiveFormatter _formatter;
        private readonly ILogger<CognitiveSynthesisProcessor> _logger;
        
        // Synthesis agent endpoints
        private const string ThematicAnalyzerUrl = "http://thematic-analyzer:80";
        private const string NarrativeWeaverUrl = "http://narrative-weaver:80";
        private const string SummarizerExpanderUrl = "http://summarizer-expander:80";
        
        public CognitiveSynthesisProcessor(
            HttpClient httpClient,
            CognitiveFormatter formatter,
            ILogger<CognitiveSynthesisProcessor> logger)
        {
            _httpClient = httpClient;
            _formatter = formatter;
            _logger = logger;
        }
        
        /// <summary>
        /// Process collected results through four-stage pipeline
        /// </summary>
        public async Task<string> ProcessAsync(
            Dictionary<string, AgentResult> collectedResults,
            float overallConfidence,
            List<string> sources,
            CancellationToken cancellationToken = default)
        {
            var sw = Stopwatch.StartNew();
            
            try
            {
                // Stage 1: Thematic Analysis
                _logger.LogInformation("Stage 1: Analyzing themes");
                var contentPlan = await AnalyzeThemesAsync(
                    collectedResults,
                    cancellationToken);
                
                // Stage 2: Narrative Weaving
                _logger.LogInformation("Stage 2: Weaving narrative");
                var coherentDraft = await WeaveNarrativeAsync(
                    contentPlan,
                    collectedResults,
                    cancellationToken);
                
                // Stage 3: Summarization & Expansion
                _logger.LogInformation("Stage 3: Creating layered response");
                var layeredResponse = await CreateLayeredResponseAsync(
                    coherentDraft,
                    overallConfidence,
                    sources,
                    cancellationToken);
                
                // Stage 4: Final Formatting
                _logger.LogInformation("Stage 4: Final formatting");
                var formattedOutput = _formatter.FormatResponse(layeredResponse);
                
                sw.Stop();
                
                _logger.LogInformation(
                    "Synthesis pipeline completed in {ElapsedMs}ms",
                    sw.ElapsedMilliseconds);
                
                return formattedOutput;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Synthesis pipeline failed");
                
                // Fallback to simple aggregation
                return FallbackAggregation(collectedResults, sources);
            }
        }
        
        /// <summary>
        /// Stage 1: Call Thematic Analyzer
        /// </summary>
        private async Task<ContentPlan> AnalyzeThemesAsync(
            Dictionary<string, AgentResult> results,
            CancellationToken cancellationToken)
        {
            var response = await _httpClient.PostAsJsonAsync(
                $"{ThematicAnalyzerUrl}/analyze_themes",
                new { CollectedResults = results },
                cancellationToken);
            
            response.EnsureSuccessStatusCode();
            
            return await response.Content.ReadFromJsonAsync<ContentPlan>(
                cancellationToken) ?? new ContentPlan();
        }
        
        /// <summary>
        /// Stage 2: Call Narrative Weaver
        /// </summary>
        private async Task<CoherentDraft> WeaveNarrativeAsync(
            ContentPlan plan,
            Dictionary<string, AgentResult> originalResults,
            CancellationToken cancellationToken)
        {
            var response = await _httpClient.PostAsJsonAsync(
                $"{NarrativeWeaverUrl}/weave_narrative",
                new { Plan = plan, OriginalResults = originalResults },
                cancellationToken);
            
            response.EnsureSuccessStatusCode();
            
            return await response.Content.ReadFromJsonAsync<CoherentDraft>(
                cancellationToken) ?? new CoherentDraft { Text = "", ParagraphCount = 0 };
        }
        
        /// <summary>
        /// Stage 3: Call Summarizer & Expander
        /// </summary>
        private async Task<LayeredResponse> CreateLayeredResponseAsync(
            CoherentDraft draft,
            float confidence,
            List<string> sources,
            CancellationToken cancellationToken)
        {
            var response = await _httpClient.PostAsJsonAsync(
                $"{SummarizerExpanderUrl}/layer_response",
                new { Draft = draft, Confidence = confidence, Sources = sources },
                cancellationToken);
            
            response.EnsureSuccessStatusCode();
            
            return await response.Content.ReadFromJsonAsync<LayeredResponse>(
                cancellationToken) ?? new LayeredResponse
                {
                    Summary = "",
                    Details = draft.Text,
                    Confidence = confidence,
                    Sources = sources,
                    RelatedTopics = new List<string>()
                };
        }
        
        /// <summary>
        /// Fallback: Simple aggregation if pipeline fails
        /// </summary>
        private string FallbackAggregation(
            Dictionary<string, AgentResult> results,
            List<string> sources)
        {
            var texts = results.Values
                .Select(r => r.Data.GetValueOrDefault("text")?.ToString())
                .Where(t => !string.IsNullOrEmpty(t));
            
            return $"{string.Join(" ", texts)}\n\nSources: {string.Join(", ", sources)}";
        }
    }
}
```

---

## Example Transformations

### Before: Simple Aggregation

**Input Query:** "Why was the lightbulb important for factories?"

**Current Output:**

```
A lightbulb is an electric device that produces light via an incandescent 
filament. The lightbulb revolutionized factory work by extending productive 
hours beyond daylight, improving worker safety through better illumination, 
and enabling 24-hour industrial operations that dramatically increased 
productivity.

Sources: Lightbulb_Definition_AI, Factory_History_AI
```

### After: Cognitive Synthesis

**Enhanced Output:**

```markdown
## Summary

The evidence strongly suggests that the lightbulb was a cornerstone of the 
industrial revolution, primarily because it enabled factories to operate 
safely and efficiently around the clock.

## Detailed Explanation

To understand this fully, it's helpful to start with the basics. A lightbulb 
is an electric device that produces reliable, controllable light through an 
incandescent filament.

Looking at the historical context, before its widespread adoption in the late 
19th century, factories were largely dependent on daylight for operations. 
Furthermore, the available alternatives—gas lamps and candles—posed 
significant fire hazards in industrial environments.

Regarding its impact, the electric lightbulb fundamentally transformed 
factory operations. Therefore, manufacturers could extend the workday beyond 
natural daylight hours, enabling the introduction of multiple shifts. As a 
result, production capacity increased dramatically, contributing to the 
rapid industrialization of the era.

In terms of safety, the lightbulb significantly improved worker conditions. 
Moreover, by replacing open flames with enclosed electric light, it 
drastically reduced fire hazards in environments often filled with 
combustible materials.

## Related Topics You Might Be Interested In

- Thomas Edison
- Industrial Revolution
- Factory Labor Conditions
- Electrical Engineering
- Workplace Safety

## Sources

Lightbulb_Definition_AI, Factory_History_AI, Industrial_Revolution_AI
```

---

## Implementation Roadmap

### Phase 1: Thematic Analysis (2 weeks)

**Goal**: Organize facts into logical themes

**Tasks:**

1. ✅ Create `ThematicAnalyzerAgent` service
2. ✅ Implement semantic clustering algorithm
3. ✅ Create ASP.NET Core endpoint
4. ✅ Integrate with Output Processor
5. ✅ Test with sample data

**Deliverable**: Facts grouped into themes

### Phase 2: Narrative Weaving (1 week)

**Goal**: Create flowing narrative

**Tasks:**

1. ✅ Create `NarrativeWeaverAgent` service
2. ✅ Implement transition logic
3. ✅ Add theme introductions
4. ✅ Test narrative quality

**Deliverable**: Coherent narrative output

### Phase 3: Layering & Expansion (2 weeks)

**Goal**: Add summary and related topics

**Tasks:**

1. ✅ Create `SummarizerExpanderAgent` service
2. ✅ Implement summarization
3. ✅ Add graph integration for related topics
4. ✅ Create `LayeredResponse` format

**Deliverable**: Rich, layered responses

### Phase 4: Final Polish (1 week)

**Goal**: Production-ready formatting

**Tasks:**

1. ✅ Enhance `CognitiveFormatter`
2. ✅ Add confidence modulation
3. ✅ Implement Markdown formatting
4. ✅ Add error handling and fallbacks

**Deliverable**: Production-ready synthesis pipeline

---

## Performance Considerations

### Latency Analysis

| Stage | Operation | Target Time | Max Acceptable |
|-------|-----------|-------------|----------------|
| Thematic Analysis | Clustering | 50ms | 150ms |
| Narrative Weaving | Text generation | 100ms | 300ms |
| Summarizer/Expander | Graph queries | 150ms | 400ms |
| Final Formatting | String operations | 10ms | 50ms |
| **Total Pipeline** | **End-to-end** | **310ms** | **900ms** |

### Optimization Strategies

1. **Parallel Processing**: Run independent operations concurrently
2. **Caching**: Cache common themes and transitions
3. **Lazy Loading**: Only fetch related topics if requested
4. **Fallback**: Quick aggregation if pipeline times out

### Resource Requirements

- **Memory**: ~100MB per synthesis operation
- **CPU**: Minimal (mostly I/O bound)
- **Network**: 3-4 internal HTTP calls
- **Graph DB**: 1-2 queries for related topics

---

**Document Version:** 1.0 C#  
**Last Updated:** 2025-01-10  
**Status:** Architecture Definition Phase

[↑ Back to Index](../INDEX.md) | [Microservices ←](microservices-csharp.md) | [Production →](production-deployment-csharp.md)
