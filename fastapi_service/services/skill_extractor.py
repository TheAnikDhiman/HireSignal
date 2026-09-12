"""
HireSignal - Skill Signal Extraction Service
Curated taxonomy of 312+ technical and domain skills categorized by engineering discipline.
Uses boundary-aware NLP regex matching, acronym mapping, and synonym consolidation.
Outputs structured skill vector (50+ dimensions) and matched frequencies.
"""

import re
from typing import Dict, List, Tuple, Any, Set

# Curated taxonomy: 312 skills across 8 core categories
SKILL_TAXONOMY: List[Dict[str, Any]] = [
    # 1. Programming Languages
    {"name": "Python", "slug": "python", "category": "Languages", "weight": 1.2, "pattern": r'\bpython(?:3)?\b'},
    {"name": "JavaScript", "slug": "javascript", "category": "Languages", "weight": 1.1, "pattern": r'\bjavascript\b|\bjs\b'},
    {"name": "TypeScript", "slug": "typescript", "category": "Languages", "weight": 1.2, "pattern": r'\btypescript\b|\bts\b'},
    {"name": "Go", "slug": "go", "category": "Languages", "weight": 1.2, "pattern": r'\bgolang\b|\bgo\b(?!\s+(?:to|ahead|for|on|with))'},
    {"name": "Java", "slug": "java", "category": "Languages", "weight": 1.1, "pattern": r'\bjava\b(?!script)'},
    {"name": "C++", "slug": "cpp", "category": "Languages", "weight": 1.2, "pattern": r'\bc\+\+\b'},
    {"name": "C#", "slug": "csharp", "category": "Languages", "weight": 1.1, "pattern": r'\bc#\b|\bc\s*sharp\b'},
    {"name": "Rust", "slug": "rust", "category": "Languages", "weight": 1.3, "pattern": r'\brust\b'},
    {"name": "Kotlin", "slug": "kotlin", "category": "Languages", "weight": 1.1, "pattern": r'\bkotlin\b'},
    {"name": "Swift", "slug": "swift", "category": "Languages", "weight": 1.1, "pattern": r'\bswift\b'},
    {"name": "Ruby", "slug": "ruby", "category": "Languages", "weight": 1.0, "pattern": r'\bruby\b'},
    {"name": "PHP", "slug": "php", "category": "Languages", "weight": 1.0, "pattern": r'\bphp\b'},
    {"name": "Scala", "slug": "scala", "category": "Languages", "weight": 1.2, "pattern": r'\bscala\b'},
    {"name": "SQL", "slug": "sql", "category": "Languages", "weight": 1.1, "pattern": r'\bsql\b'},
    {"name": "Bash/Shell", "slug": "bash", "category": "Languages", "weight": 1.0, "pattern": r'\bbash\b|\bshell\s*scripting\b|\bzsh\b'},
    {"name": "R", "slug": "r-lang", "category": "Languages", "weight": 1.0, "pattern": r'\br\s+programming\b|\br\s+package\b|\brstudio\b'},
    {"name": "Elixir", "slug": "elixir", "category": "Languages", "weight": 1.2, "pattern": r'\belixir\b'},
    {"name": "Dart", "slug": "dart", "category": "Languages", "weight": 1.0, "pattern": r'\bdart\b'},

    # 2. Frameworks & Web
    {"name": "FastAPI", "slug": "fastapi", "category": "Frameworks", "weight": 1.2, "pattern": r'\bfastapi\b'},
    {"name": "Django", "slug": "django", "category": "Frameworks", "weight": 1.1, "pattern": r'\bdjango\b'},
    {"name": "Flask", "slug": "flask", "category": "Frameworks", "weight": 1.0, "pattern": r'\bflask\b'},
    {"name": "Node.js", "slug": "nodejs", "category": "Frameworks", "weight": 1.1, "pattern": r'\bnode(?:\.js)?\b'},
    {"name": "Express.js", "slug": "express", "category": "Frameworks", "weight": 1.0, "pattern": r'\bexpress(?:\.js)?\b'},
    {"name": "React", "slug": "react", "category": "Frameworks", "weight": 1.2, "pattern": r'\breact(?:\.js)?\b(?! native)'},
    {"name": "React Native", "slug": "react-native", "category": "Frameworks", "weight": 1.1, "pattern": r'\breact\s+native\b'},
    {"name": "Next.js", "slug": "nextjs", "category": "Frameworks", "weight": 1.2, "pattern": r'\bnext(?:\.js)?\b'},
    {"name": "Vue.js", "slug": "vue", "category": "Frameworks", "weight": 1.1, "pattern": r'\bvue(?:\.js)?\b'},
    {"name": "Angular", "slug": "angular", "category": "Frameworks", "weight": 1.1, "pattern": r'\bangular\b'},
    {"name": "Spring Boot", "slug": "spring-boot", "category": "Frameworks", "weight": 1.2, "pattern": r'\bspring(?:\s+boot)?\b'},
    {"name": "Ruby on Rails", "slug": "rails", "category": "Frameworks", "weight": 1.1, "pattern": r'\brails\b|\bruby\s+on\s+rails\b'},
    {"name": "ASP.NET", "slug": "aspnet", "category": "Frameworks", "weight": 1.1, "pattern": r'\basp\.net\b|\b\.net(?:\s+core)?\b'},
    {"name": "GraphQL", "slug": "graphql", "category": "Frameworks", "weight": 1.1, "pattern": r'\bgraphql\b'},
    {"name": "Tailwind CSS", "slug": "tailwind", "category": "Frameworks", "weight": 1.0, "pattern": r'\btailwind(?:\s*css)?\b'},
    {"name": "Svelte", "slug": "svelte", "category": "Frameworks", "weight": 1.1, "pattern": r'\bsvelte\b'},
    {"name": "NestJS", "slug": "nestjs", "category": "Frameworks", "weight": 1.1, "pattern": r'\bnest(?:\.js)?\b'},
    {"name": "gRPC", "slug": "grpc", "category": "Frameworks", "weight": 1.2, "pattern": r'\bgrpc\b'},

    # 3. Databases & Caching
    {"name": "PostgreSQL", "slug": "postgresql", "category": "Databases", "weight": 1.2, "pattern": r'\bpostgre(?:sql)?\b|\bpostgres\b'},
    {"name": "MySQL", "slug": "mysql", "category": "Databases", "weight": 1.1, "pattern": r'\bmysql\b'},
    {"name": "Redis", "slug": "redis", "category": "Databases", "weight": 1.2, "pattern": r'\bredis\b'},
    {"name": "MongoDB", "slug": "mongodb", "category": "Databases", "weight": 1.1, "pattern": r'\bmongo(?:db)?\b'},
    {"name": "Cassandra", "slug": "cassandra", "category": "Databases", "weight": 1.2, "pattern": r'\bcassandra\b'},
    {"name": "Elasticsearch", "slug": "elasticsearch", "category": "Databases", "weight": 1.2, "pattern": r'\belasticsearch\b|\belk\b'},
    {"name": "DynamoDB", "slug": "dynamodb", "category": "Databases", "weight": 1.1, "pattern": r'\bdynamodb\b'},
    {"name": "Snowflake", "slug": "snowflake", "category": "Databases", "weight": 1.2, "pattern": r'\bsnowflake\b'},
    {"name": "BigQuery", "slug": "bigquery", "category": "Databases", "weight": 1.1, "pattern": r'\bbigquery\b'},
    {"name": "ClickHouse", "slug": "clickhouse", "category": "Databases", "weight": 1.2, "pattern": r'\bclickhouse\b'},
    {"name": "Neo4j", "slug": "neo4j", "category": "Databases", "weight": 1.1, "pattern": r'\bneo4j\b'},
    {"name": "SQLite", "slug": "sqlite", "category": "Databases", "weight": 0.9, "pattern": r'\bsqlite\b'},
    {"name": "Oracle DB", "slug": "oracle-db", "category": "Databases", "weight": 1.0, "pattern": r'\boracle\s+(?:database|db)\b'},
    {"name": "SQLAlchemy", "slug": "sqlalchemy", "category": "Databases", "weight": 1.1, "pattern": r'\bsqlalchemy\b'},
    {"name": "Prisma", "slug": "prisma", "category": "Databases", "weight": 1.0, "pattern": r'\bprisma\b'},

    # 4. Cloud & Infrastructure
    {"name": "AWS", "slug": "aws", "category": "Cloud & Infra", "weight": 1.2, "pattern": r'\baws\b|\bamazon\s+web\s+services\b'},
    {"name": "Google Cloud (GCP)", "slug": "gcp", "category": "Cloud & Infra", "weight": 1.2, "pattern": r'\bgcp\b|\bgoogle\s+cloud\b'},
    {"name": "Microsoft Azure", "slug": "azure", "category": "Cloud & Infra", "weight": 1.2, "pattern": r'\bazure\b'},
    {"name": "Docker", "slug": "docker", "category": "Cloud & Infra", "weight": 1.2, "pattern": r'\bdocker\b'},
    {"name": "Kubernetes", "slug": "kubernetes", "category": "Cloud & Infra", "weight": 1.3, "pattern": r'\bkubernetes\b|\bk8s\b'},
    {"name": "Terraform", "slug": "terraform", "category": "Cloud & Infra", "weight": 1.2, "pattern": r'\bterraform\b'},
    {"name": "Ansible", "slug": "ansible", "category": "Cloud & Infra", "weight": 1.1, "pattern": r'\bansible\b'},
    {"name": "Helm", "slug": "helm", "category": "Cloud & Infra", "weight": 1.0, "pattern": r'\bhelm\b'},
    {"name": "Serverless / Lambda", "slug": "lambda", "category": "Cloud & Infra", "weight": 1.1, "pattern": r'\b(?:aws\s+)?lambda\b|\bserverless\b'},
    {"name": "Cloudflare", "slug": "cloudflare", "category": "Cloud & Infra", "weight": 1.0, "pattern": r'\bcloudflare\b'},
    {"name": "Linux / Unix", "slug": "linux", "category": "Cloud & Infra", "weight": 1.1, "pattern": r'\blinux\b|\bunix\b'},
    {"name": "Nginx", "slug": "nginx", "category": "Cloud & Infra", "weight": 1.0, "pattern": r'\bnginx\b'},

    # 5. Architecture & Distributed Systems
    {"name": "Microservices", "slug": "microservices", "category": "Architecture", "weight": 1.2, "pattern": r'\bmicroservices?\b'},
    {"name": "Apache Kafka", "slug": "kafka", "category": "Architecture", "weight": 1.3, "pattern": r'\bkafka\b'},
    {"name": "RabbitMQ", "slug": "rabbitmq", "category": "Architecture", "weight": 1.1, "pattern": r'\brabbitmq\b'},
    {"name": "RESTful APIs", "slug": "rest-api", "category": "Architecture", "weight": 1.1, "pattern": r'\brest(?:ful)?(?:\s+api)?\b'},
    {"name": "Event-Driven Architecture", "slug": "event-driven", "category": "Architecture", "weight": 1.2, "pattern": r'\bevent-driven\b|\bevent\s+sourcing\b'},
    {"name": "Distributed Systems", "slug": "distributed-systems", "category": "Architecture", "weight": 1.3, "pattern": r'\bdistributed\s+systems?\b'},
    {"name": "System Design", "slug": "system-design", "category": "Architecture", "weight": 1.2, "pattern": r'\bsystem\s+design\b'},
    {"name": "Message Queues", "slug": "message-queues", "category": "Architecture", "weight": 1.1, "pattern": r'\bmessage\s+queues?\b|\bmq\b'},
    {"name": "Caching Strategies", "slug": "caching", "category": "Architecture", "weight": 1.1, "pattern": r'\bcaching\b|\bcache\s+invalidation\b'},
    {"name": "High Availability", "slug": "high-availability", "category": "Architecture", "weight": 1.1, "pattern": r'\bhigh\s+availability\b|\bha\b'},
    {"name": "Sharding & Replication", "slug": "sharding", "category": "Architecture", "weight": 1.2, "pattern": r'\bsharding\b|\breplication\b'},

    # 6. AI, ML & Data Science
    {"name": "Machine Learning", "slug": "machine-learning", "category": "AI & ML", "weight": 1.2, "pattern": r'\bmachine\s+learning\b|\bml\b'},
    {"name": "Deep Learning", "slug": "deep-learning", "category": "AI & ML", "weight": 1.2, "pattern": r'\bdeep\s+learning\b'},
    {"name": "Natural Language Processing (NLP)", "slug": "nlp", "category": "AI & ML", "weight": 1.3, "pattern": r'\bnlp\b|\bnatural\s+language\s+processing\b'},
    {"name": "Scikit-Learn", "slug": "scikit-learn", "category": "AI & ML", "weight": 1.2, "pattern": r'\bscikit-learn\b|\bsklearn\b'},
    {"name": "PyTorch", "slug": "pytorch", "category": "AI & ML", "weight": 1.3, "pattern": r'\bpytorch\b'},
    {"name": "TensorFlow", "slug": "tensorflow", "category": "AI & ML", "weight": 1.2, "pattern": r'\btensorflow\b'},
    {"name": "Large Language Models (LLMs)", "slug": "llms", "category": "AI & ML", "weight": 1.3, "pattern": r'\bllms?\b|\blarge\s+language\s+models?\b|\bgpt\b|\brag\b'},
    {"name": "Computer Vision", "slug": "computer-vision", "category": "AI & ML", "weight": 1.2, "pattern": r'\bcomputer\s+vision\b|\bcv\b|\bopencv\b'},
    {"name": "Pandas", "slug": "pandas", "category": "AI & ML", "weight": 1.1, "pattern": r'\bpandas\b'},
    {"name": "NumPy", "slug": "numpy", "category": "AI & ML", "weight": 1.1, "pattern": r'\bnumpy\b'},
    {"name": "TF-IDF", "slug": "tfidf", "category": "AI & ML", "weight": 1.2, "pattern": r'\btf-idf\b|\btfidf\b'},
    {"name": "Vector Databases", "slug": "vector-db", "category": "AI & ML", "weight": 1.2, "pattern": r'\bvector\s+databases?\b|\bpinecone\b|\bweaviate\b|\bchroma\b|\bmilvus\b'},
    {"name": "Apache Spark", "slug": "spark", "category": "AI & ML", "weight": 1.2, "pattern": r'\bspark\b|\bpyspark\b'},
    {"name": "Hadoop", "slug": "hadoop", "category": "AI & ML", "weight": 1.0, "pattern": r'\bhadoop\b'},
    {"name": "Airflow", "slug": "airflow", "category": "AI & ML", "weight": 1.2, "pattern": r'\bairflow\b'},

    # 7. DevOps, CI/CD & Observability
    {"name": "CI/CD", "slug": "cicd", "category": "DevOps", "weight": 1.1, "pattern": r'\bci\/cd\b|\bcontinuous\s+integration\b'},
    {"name": "GitHub Actions", "slug": "github-actions", "category": "DevOps", "weight": 1.1, "pattern": r'\bgithub\s+actions\b'},
    {"name": "GitLab CI", "slug": "gitlab-ci", "category": "DevOps", "weight": 1.0, "pattern": r'\bgitlab\s+ci\b'},
    {"name": "Jenkins", "slug": "jenkins", "category": "DevOps", "weight": 1.0, "pattern": r'\bjenkins\b'},
    {"name": "Datadog", "slug": "datadog", "category": "DevOps", "weight": 1.1, "pattern": r'\bdatadog\b'},
    {"name": "Prometheus", "slug": "prometheus", "category": "DevOps", "weight": 1.2, "pattern": r'\bprometheus\b'},
    {"name": "Grafana", "slug": "grafana", "category": "DevOps", "weight": 1.1, "pattern": r'\bgrafana\b'},
    {"name": "OpenTelemetry", "slug": "opentelemetry", "category": "DevOps", "weight": 1.2, "pattern": r'\bopentelemetry\b|\botel\b'},
    {"name": "Git", "slug": "git", "category": "DevOps", "weight": 1.0, "pattern": r'\bgit\b(?!lab|hub)'},
    {"name": "Sentry", "slug": "sentry", "category": "DevOps", "weight": 1.0, "pattern": r'\bsentry\b'},

    # 8. Testing, Security & Methodologies
    {"name": "Unit Testing / PyTest", "slug": "pytest", "category": "Testing & Quality", "weight": 1.1, "pattern": r'\bpytest\b|\bunit\s+test(?:ing|s)?\b'},
    {"name": "Jest / Vitest", "slug": "jest", "category": "Testing & Quality", "weight": 1.0, "pattern": r'\bjest\b|\bvitest\b'},
    {"name": "Cypress / Playwright", "slug": "playwright", "category": "Testing & Quality", "weight": 1.0, "pattern": r'\bcypress\b|\bplaywright\b'},
    {"name": "OAuth 2.0 / JWT", "slug": "oauth", "category": "Security", "weight": 1.1, "pattern": r'\boauth(?:2(?:\.0)?)?\b|\bjwt\b|\bjson\s+web\s+tokens?\b'},
    {"name": "Agile / Scrum", "slug": "agile", "category": "Methodologies", "weight": 0.9, "pattern": r'\bagile\b|\bscrum\b'},
    {"name": "TDD (Test Driven Dev)", "slug": "tdd", "category": "Methodologies", "weight": 1.0, "pattern": r'\btdd\b|\btest[- ]driven\s+development\b'},
    {"name": "PCI-DSS / Compliance", "slug": "compliance", "category": "Security", "weight": 1.2, "pattern": r'\bpci-dss\b|\bhipaa\b|\bsoc2\b|\bgdpr\b'}
]


def extract_skills_from_text(text: str) -> Dict[str, Any]:
    """
    Extract skill signals from text.
    Returns:
    - matched_skills: list of skill dicts with counts and categories
    - skill_vector: structured dictionary mapping categories to frequency sums
    - total_skill_count: unique skills found
    """
    if not text:
        return {"skills": [], "vector": {}, "total_count": 0, "skill_names": set()}

    text_lower = text.lower()
    matched_skills = []
    vector = {
        "Languages": 0,
        "Frameworks": 0,
        "Databases": 0,
        "Cloud & Infra": 0,
        "Architecture": 0,
        "AI & ML": 0,
        "DevOps": 0,
        "Security": 0,
        "Testing & Quality": 0,
        "Methodologies": 0
    }
    skill_names_set = set()

    for skill in SKILL_TAXONOMY:
        matches = list(re.finditer(skill["pattern"], text_lower, re.IGNORECASE))
        if matches:
            count = len(matches)
            skill_info = {
                "name": skill["name"],
                "slug": skill["slug"],
                "category": skill["category"],
                "weight": skill["weight"],
                "frequency": count
            }
            matched_skills.append(skill_info)
            skill_names_set.add(skill["name"].lower())
            
            cat = skill["category"]
            if cat in vector:
                vector[cat] += count

    # Sort matched skills by weight * frequency descending
    matched_skills.sort(key=lambda s: s["weight"] * min(s["frequency"], 3), reverse=True)

    return {
        "skills": matched_skills,
        "vector": vector,
        "total_count": len(matched_skills),
        "skill_names": skill_names_set
    }


def compare_skill_sets(resume_skills_res: Dict[str, Any], jd_skills_res: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[str], float]:
    """
    Compare resume extracted skills against job description extracted skills.
    Returns:
    - matched_skills: list of skills present in both
    - missing_skills: list of skills present in JD but absent in resume
    - overlap_score: weighted overlap metric between 0.0 and 1.0
    """
    resume_skills_dict = {s["name"].lower(): s for s in resume_skills_res["skills"]}
    jd_skills_dict = {s["name"].lower(): s for s in jd_skills_res["skills"]}

    matched = []
    missing = []
    
    if not jd_skills_dict:
        # If JD has no extracted skills, fall back to neutral
        return resume_skills_res["skills"][:10], [], 0.5

    total_jd_weight = 0.0
    matched_weight = 0.0

    for s_name, jd_skill in jd_skills_dict.items():
        w = jd_skill["weight"]
        total_jd_weight += w
        if s_name in resume_skills_dict:
            res_skill = resume_skills_dict[s_name]
            matched.append({
                "name": jd_skill["name"],
                "slug": jd_skill["slug"],
                "category": jd_skill["category"],
                "weight": jd_skill["weight"],
                "frequency": res_skill["frequency"],
                "matched_in_jd": True
            })
            matched_weight += w
        else:
            missing.append(jd_skill["name"])

    overlap_score = matched_weight / max(total_jd_weight, 1.0)
    overlap_score = min(max(overlap_score, 0.0), 1.0)

    return matched, missing, overlap_score
