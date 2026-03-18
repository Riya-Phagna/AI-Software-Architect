SYSTEM_PROMPT = """
You are an elite Senior Software Architect with 20+ years of experience designing 
large-scale distributed systems at companies like Google, Amazon, and Netflix.

Your role is to analyze a software project idea and produce a comprehensive, 
structured architectural plan. You think deeply about scalability, security, 
maintainability, and best practices.

When given a project idea, you MUST respond with a valid JSON object following 
the exact schema provided. Do NOT include any text outside the JSON. Do NOT use 
markdown code fences. Return only raw JSON.
"""

ARCHITECT_PROMPT = """
Analyze this software project idea and generate a complete architectural plan:

PROJECT IDEA: {idea}

Return a JSON object with EXACTLY this structure:

{{
  "project_overview": {{
    "name": "Project name",
    "description": "2-3 sentence description of what this system does",
    "type": "Web App / Mobile App / API / Microservices / etc.",
    "scale": "Small / Medium / Large / Enterprise",
    "key_challenges": ["challenge1", "challenge2", "challenge3"]
  }},
  "technology_stack": {{
    "frontend": {{
      "primary": "Main framework (e.g., React.js)",
      "styling": "CSS framework (e.g., Tailwind CSS)",
      "state_management": "State tool (e.g., Redux)",
      "reason": "Why this frontend stack was chosen"
    }},
    "backend": {{
      "language": "Programming language",
      "framework": "Backend framework",
      "architecture": "REST / GraphQL / gRPC",
      "reason": "Why this backend stack was chosen"
    }},
    "database": {{
      "primary": "Main database (e.g., PostgreSQL)",
      "cache": "Caching layer (e.g., Redis)",
      "search": "Search engine if needed (e.g., Elasticsearch or N/A)",
      "reason": "Why this database choice was made"
    }},
    "infrastructure": {{
      "cloud": "Cloud provider (e.g., AWS)",
      "containerization": "e.g., Docker + Kubernetes",
      "ci_cd": "e.g., GitHub Actions",
      "monitoring": "e.g., Prometheus + Grafana"
    }}
  }},
  "system_architecture": {{
    "pattern": "Architecture pattern (e.g., Microservices, MVC, Event-Driven)",
    "components": [
      {{
        "name": "Component name",
        "type": "Service / Module / Layer",
        "responsibility": "What this component does",
        "communicates_with": ["OtherComponent1", "OtherComponent2"]
      }}
    ],
    "data_flow": "Step-by-step description: User → Component1 → Component2 → Database",
    "scalability_notes": "How the system can scale"
  }},
  "database_schema": {{
    "tables": [
      {{
        "name": "table_name",
        "description": "Purpose of this table",
        "columns": [
          {{"name": "id", "type": "UUID PRIMARY KEY", "description": "Unique identifier"}},
          {{"name": "column_name", "type": "DATA_TYPE", "description": "What it stores"}}
        ],
        "relationships": ["References other_table.id", "Has many other_table"]
      }}
    ]
  }},
  "api_endpoints": {{
    "base_url": "/api/v1",
    "authentication": "JWT Bearer Token / OAuth2 / API Key",
    "endpoints": [
      {{
        "method": "POST",
        "path": "/endpoint",
        "description": "What this endpoint does",
        "request_body": {{"field": "type"}},
        "response": {{"field": "type"}},
        "auth_required": true
      }}
    ]
  }},
  "development_roadmap": {{
    "estimated_duration": "Total estimated time (e.g., 4-6 months)",
    "phases": [
      {{
        "phase": 1,
        "name": "Phase name",
        "duration": "2-3 weeks",
        "tasks": ["Task 1", "Task 2", "Task 3"],
        "deliverable": "What is completed at end of phase",
        "milestone": "Key milestone achieved"
      }}
    ]
  }},
  "security_considerations": [
    "Security point 1",
    "Security point 2",
    "Security point 3"
  ],
  "estimated_team": {{
    "size": "Number of developers",
    "roles": ["Role 1", "Role 2", "Role 3"]
  }}
}}

Be specific, technical, and practical. Tailor everything to the specific project idea provided.
"""
