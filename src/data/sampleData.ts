import { PresetResume, PresetJobDescription } from '../types';

export const PRESET_RESUMES: PresetResume[] = [
  {
    id: 'priya_sharma',
    name: 'Priya Sharma',
    title: 'Senior Backend Engineer (Payments & Distributed Systems)',
    experienceYears: 6.5,
    fileName: 'priya_sharma_resume.pdf',
    summary: '6+ years specializing in high-throughput payments, Go, Python, Kafka, and PostgreSQL. Low red flags, high technical fit for fintech.',
    text: `Priya Sharma
San Francisco, CA | priya.sharma@example.com | (415) 555-0192
linkedin.com/in/priyasharma-dev | github.com/priyasharma-payments

PROFESSIONAL SUMMARY
Senior Backend Engineer with 6+ years of experience building high-throughput payment processing architectures, distributed transaction systems, and mission-critical financial APIs. Proven track record scaling microservices in Python, Go, and PostgreSQL handling over 18,000 requests/sec with 99.995% uptime.

TECHNICAL SKILLS
• Languages: Python, Go (Golang), SQL, TypeScript, Bash
• Frameworks: FastAPI, Django, gRPC, Node.js, Express.js
• Databases & Caching: PostgreSQL, Redis, DynamoDB, Elasticsearch
• Cloud & Infrastructure: AWS (ECS, Lambda, RDS, S3), Docker, Kubernetes (k8s), Terraform
• Architecture & Messaging: Apache Kafka, Event-Driven Architecture, Microservices, RESTful APIs, Distributed Systems
• Observability & DevOps: Datadog, Prometheus, Grafana, OpenTelemetry, CI/CD, GitHub Actions
• Testing & Compliance: PyTest, Unit Testing, PCI-DSS compliance, OAuth 2.0, JWT

PROFESSIONAL EXPERIENCE

Senior Backend Engineer | PayScale Financial Technologies
San Francisco, CA | 2021 – Present
• Architected and launched high-volume payment settlement pipeline using Python (FastAPI), Go, and Apache Kafka, processing $42M+ daily transaction volume.
• Redesigned distributed database schema in PostgreSQL with automated read replicas and Redis caching tier, decreasing p99 API latency from 420ms to 68ms (84% reduction).
• Containerized core payments microservices using Docker and deployed onto Amazon EKS with Terraform IaC, achieving zero-downtime rolling deployments.
• Spearheaded migration from legacy monolithic REST endpoints to event-driven gRPC streaming, increasing transaction throughput by 3.4x.
• Implemented end-to-end PCI-DSS Level 1 tokenization and cryptographic signature validation using OAuth 2.0 and JWT.

Software Engineer | FinFlow Systems
New York, NY | 2018 – 2021
• Developed multi-currency ledger reconciliation service in Python and PostgreSQL, automating end-of-day settlement for 120,000+ merchant accounts.
• Engineered asynchronous webhook delivery system backed by RabbitMQ and Redis, delivering 99.99% message delivery reliability under peak load.
• Configured Datadog APM dashboards, Prometheus custom metrics, and PagerDuty alert escalation paths, reducing MTTR by 35%.
• Authored comprehensive PyTest test suites with 92% code coverage across all financial ledger repositories.

EDUCATION
B.S. in Computer Science | University of California, Berkeley (2014 – 2018)`
  },
  {
    id: 'alex_chen',
    name: 'Alex Chen',
    title: 'Junior Full-Stack Developer',
    experienceYears: 1.5,
    fileName: 'alex_chen_cv.docx',
    summary: 'Junior engineer with strong React & Node skills, but exhibits generic objective statement, vague non-metric bullet points, and minor ATS red flags.',
    text: `Alex Chen
Austin, TX | alex.chen.dev99@gmail.com | (512) 555-8391
github.com/alexchen-web

OBJECTIVE
Seeking a challenging entry-level or junior software engineering role in a dynamic, esteemed technology organization where I can utilize my programming skills and learn new technologies while contributing to company success.

SKILLS
React, JavaScript, TypeScript, HTML, CSS, Tailwind CSS, Node.js, Express.js, MongoDB, Git, GitHub, REST APIs, JSON, Postman, Jest

EXPERIENCE

Junior Frontend Developer | Apex Interactive
Austin, TX | 2023 – Present
• Worked on building modern web applications using React, TypeScript, and Tailwind CSS for client landing pages.
• Helped my team integrate RESTful APIs to display user dashboards and account profile pages.
• Fixed multiple user-facing UI bugs and contributed to daily standup meetings.
• Collaborated with designers to convert Figma prototypes into responsive web components.
• Tested frontend components using Jest and ensured good cross-browser performance on mobile devices.

Web Development Intern | CloudStart Studios
Austin, TX | 2022 – 2023
• Assisted senior engineers in writing backend endpoints in Node.js and Express.js.
• Created database queries for MongoDB collections and structured JSON payloads.
• Maintained documentation and updated repository README files.

EDUCATION
B.A. in Digital Media & Computing | University of Texas at Austin (2019 – 2023)`
  },
  {
    id: 'sarah_jenkins',
    name: 'Sarah Jenkins',
    title: 'Staff Cloud Infrastructure & DevOps Architect',
    experienceYears: 9.0,
    fileName: 'sarah_jenkins_lead_devops.pdf',
    summary: '9+ years architecting Kubernetes clusters, multi-region AWS/GCP, Datadog observability, and Terraform infrastructure as code.',
    text: `Sarah Jenkins
Seattle, WA | sarah.jenkins.cloud@gmail.com | (206) 555-7319
linkedin.com/in/sarah-jenkins-sre | github.com/sjenkins-cloud

EXECUTIVE SUMMARY
Staff Site Reliability & Cloud Infrastructure Architect with 9+ years directing cloud platform modernization, multi-cluster Kubernetes deployments, and automated GitOps workflows. Designed high-availability infrastructure supporting 150M monthly active users across AWS and GCP.

CORE COMPETENCIES
• Cloud & Orchestration: AWS, GCP, Kubernetes (k8s), Docker, Terraform, Helm, Ansible, Linux
• Observability: Datadog, Prometheus, Grafana, OpenTelemetry, Alertmanager, CloudWatch
• CI/CD & Automation: GitHub Actions, GitLab CI, ArgoCD, Git, Bash scripting, Python
• Distributed Systems & Storage: PostgreSQL, Redis, Elasticsearch, Kafka, Nginx
• Security & Governance: SOC2 compliance, IAM, Zero-Trust Architecture, HashiCorp Vault

WORK EXPERIENCE

Lead Infrastructure Architect | CloudScale Networks
Seattle, WA | 2020 – Present
• Designed and provisioned multi-region AWS and Kubernetes platform using Terraform and Helm, cutting annual cloud compute expenditure by $1.8M (32% savings).
• Automated zero-downtime blue/green deployment pipelines with ArgoCD and GitHub Actions, scaling deployment frequency from weekly to 45+ daily releases.
• Built enterprise-wide observability platform with Datadog, OpenTelemetry, and Prometheus, tracking 400+ microservices and driving MTTR down from 54 minutes to 8 minutes.
• Orchestrated chaos engineering drills using Chaos Mesh, uncovering 14 single-points-of-failure before production holiday traffic spikes.

Senior DevOps Engineer | DataStream Global
Seattle, WA | 2016 – 2020
• Migrated 60+ legacy bare-metal server applications into Dockerized microservices deployed on Google Cloud Kubernetes Engine (GKE).
• Standardized CI/CD testing pipelines with PyTest and container scanning, reducing broken build rates by 70%.
• Managed high-availability PostgreSQL and Redis replication clusters across multiple availability zones with automated failover testing.

EDUCATION
B.S. in Computer Engineering | University of Washington (2012 – 2016)`
  },
  {
    id: 'marcus_vance',
    name: 'Marcus Vance',
    title: 'Machine Learning & NLP Research Engineer',
    experienceYears: 5.0,
    fileName: 'marcus_vance_ml_cv.pdf',
    summary: '5 years deploying PyTorch foundation models, TF-IDF / vector search pipelines, Scikit-learn classifiers, and distributed retrieval architectures.',
    text: `Marcus Vance
Boston, MA | marcus.vance.ai@gmail.com | (617) 555-9024
github.com/marcusvance-ml | linkedin.com/in/marcusvance-ai

PROFESSIONAL SUMMARY
Machine Learning Engineer specializing in Natural Language Processing (NLP), Large Language Model (LLM) fine-tuning, and semantic retrieval systems. 5+ years shipping deep learning pipelines in PyTorch, Scikit-learn, and FastAPI powering real-time inference at scale.

TECHNICAL STACK
• AI / Machine Learning: PyTorch, Scikit-learn, HuggingFace, TensorFlow, NLP, TF-IDF, Vector Databases (Pinecone, Chroma), LangChain
• Programming: Python, SQL, C++, Bash
• Data & Backend: Pandas, NumPy, FastAPI, PostgreSQL, Redis, Docker, AWS, Spark
• Methodologies: MLOps, Model Quantization (LoRA, QLoRA), A/B Testing, PyTest

PROFESSIONAL EXPERIENCE

Senior ML Engineer | Cognition Labs
Boston, MA | 2022 – Present
• Fine-tuned 7B and 13B open-weights LLMs for domain-specific contract analysis, boosting extractive accuracy from 71% to 89.4% F1 score.
• Architected real-time hybrid search retrieval service combining TF-IDF lexical matching and dense vector embeddings, reducing search latency to 42ms.
• Deployed high-throughput model inference endpoints on AWS EC2 GPU instances using FastAPI and Docker, servicing 3,000 queries per minute.
• Implemented automated model drift evaluation pipelines with Pandas and Scikit-learn, triggering automated retraining when validation loss drifted > 5%.

Machine Learning Engineer | SemanticData Systems
Cambridge, MA | 2019 – 2022
• Trained multi-label text classification models using Scikit-learn (OneVsRest Logistic Regression and SVM), processing 500,000 support tickets monthly.
• Built distributed feature store using PostgreSQL and Redis, cutting feature preparation latency by 65%.
• Collaborated with data engineering team to ingest raw datasets with PySpark, maintaining 99.8% ETL pipeline availability.

EDUCATION
M.S. in Artificial Intelligence | Massachusetts Institute of Technology (2017 – 2019)
B.S. in Applied Mathematics | Brown University (2013 – 2017)`
  }
];

export const PRESET_JOBS: PresetJobDescription[] = [
  {
    id: 'stripe_payments',
    title: 'Senior Backend Engineer — Payments Platform',
    company: 'Stripe',
    seniority: 'Senior',
    location: 'San Francisco, CA / Remote',
    text: `Senior Backend Engineer — Payments Platform
Company: Stripe
Location: San Francisco, CA / Remote

About The Role:
We are looking for an experienced Senior Backend Engineer to join our Payments Platform team. In this role, you will design, build, and operate distributed systems that process hundreds of billions of dollars each year for millions of businesses worldwide. You will be responsible for low-latency transaction processing, bulletproof consistency, and building resilient APIs.

Responsibilities:
• Architect, build, and scale low-latency backend microservices using Python, Go, and PostgreSQL.
• Design event-driven pipelines using Apache Kafka and message queues to power real-time settlement and authorization flows.
• Implement distributed caching strategies with Redis to maintain sub-100ms response times globally.
• Deploy and manage containerized services using Docker, Kubernetes (EKS), and Terraform on AWS.
• Ensure adherence to strict financial regulatory standards, security benchmarks, and PCI-DSS compliance.
• Instrument deep observability across services using Datadog, Prometheus, Grafana, and OpenTelemetry.
• Collaborate with cross-functional engineering leads to drive high-availability architectural design reviews.

Requirements:
• 4+ years of professional backend software engineering experience.
• Strong proficiency in Python or Go, with deep familiarity in modern backend frameworks (such as FastAPI, Django, or gRPC).
• Extensive hands-on experience with relational databases (specifically PostgreSQL) and distributed SQL query optimization.
• Solid background in distributed systems, event-driven architecture, and asynchronous messaging with Apache Kafka.
• Experience with cloud infrastructure (AWS or GCP), Docker containerization, and Kubernetes orchestration.
• Familiarity with security protocols, OAuth 2.0, authentication standards, and financial compliance.
• Dedication to test-driven development (TDD), automated CI/CD pipelines, and robust code quality.`
  },
  {
    id: 'airbnb_fullstack',
    title: 'Staff Full-Stack Engineer — Guest Experience',
    company: 'Airbnb',
    seniority: 'Staff',
    location: 'San Francisco, CA / Hybrid',
    text: `Staff Full-Stack Engineer — Guest Experience
Company: Airbnb
Location: San Francisco, CA

About The Role:
As a Staff Full-Stack Engineer on the Guest Experience team, you will lead the evolution of Airbnb's core booking and exploration web platforms. You will bridge elegant frontend experiences with resilient, distributed backend services that support hundreds of millions of travelers globally.

Key Responsibilities:
• Lead the technical vision and architectural design for guest discovery interfaces using React, Next.js, and TypeScript.
• Build scalable backend microservices in Java or Node.js connected to GraphQL federation and RESTful APIs.
• Optimize client-side rendering performance, Core Web Vitals, and responsive UI components using modern Tailwind CSS.
• Partner with product management, data scientists, and design teams to run large-scale A/B experiments.
• Champion automated testing practices (Jest, Cypress), CI/CD pipelines with GitHub Actions, and high code quality.

Requirements:
• 6+ years of full-stack software development experience.
• Deep mastery of modern JavaScript/TypeScript, React, Next.js, and state management paradigms.
• Strong backend experience building APIs with Node.js, Express, or Java / Spring Boot.
• Proven expertise with relational databases (PostgreSQL, MySQL) and caching systems (Redis).
• Track record leading large-scale architectural projects, mentoring mid-level engineers, and driving cross-team alignment.`
  },
  {
    id: 'datadog_sre',
    title: 'Site Reliability Engineer — Cloud Infrastructure',
    company: 'Datadog',
    seniority: 'Senior',
    location: 'New York, NY / Remote',
    text: `Site Reliability Engineer — Cloud Infrastructure
Company: Datadog
Location: New York, NY / Remote

About The Team:
Datadog is the monitoring and security platform for cloud applications. Our SRE teams ensure that our massive, multi-cloud infrastructure operates seamlessly 24/7/365, ingesting trillions of telemetry events daily across Kubernetes clusters worldwide.

What You'll Do:
• Architect, scale, and maintain large-scale Kubernetes clusters running on AWS and GCP.
• Author robust Infrastructure as Code (IaC) using Terraform, Helm, and Ansible.
• Develop automation tooling and controllers in Go or Python to self-heal infrastructure anomalies.
• Implement real-time monitoring, alerting, and telemetry dashboards using Datadog APM, Prometheus, and Grafana.
• Lead incident triage, root cause analysis (RCA), and implement preventive engineering measures.
• Drive GitOps adoption with CI/CD automation pipelines using GitHub Actions or GitLab CI.

Requirements:
• 4+ years in Site Reliability Engineering, DevOps, or Systems Engineering.
• Expert proficiency with Linux systems, networking protocols, and container runtimes (Docker, Kubernetes).
• Advanced Terraform and cloud orchestration experience across AWS or GCP.
• Strong coding skills in Go, Python, or Bash for systems automation.
• Experience troubleshooting complex distributed systems issues and handling high-concurrency production outages.`
  },
  {
    id: 'openai_ml',
    title: 'Machine Learning Engineer — Retrieval & Systems',
    company: 'OpenAI',
    seniority: 'Senior',
    location: 'San Francisco, CA',
    text: `Machine Learning Engineer — Retrieval & Systems
Company: OpenAI
Location: San Francisco, CA

About The Role:
We are seeking an experienced Machine Learning Engineer to join our Retrieval and Foundation Systems team. You will research, build, and deploy high-performance retrieval architectures combining dense vector representations, hybrid lexical search (TF-IDF), and large-scale model inference pipelines.

Responsibilities:
• Design and scale distributed vector retrieval systems and low-latency embeddings search using PyTorch, Scikit-learn, and Vector Databases.
• Build real-time model inference services in Python and FastAPI running on GPU-accelerated Kubernetes clusters.
• Optimize model fine-tuning workflows, quantization techniques (LoRA), and evaluation benchmarks for Natural Language Processing (NLP).
• Implement robust caching layers using Redis and high-throughput data processing pipelines with Pandas and Spark.
• Collaborate closely with research scientists to take frontier AI prototypes into production-grade systems.

Qualifications:
• 4+ years of professional Machine Learning engineering experience.
• Strong expertise in Python, PyTorch, Scikit-learn, and modern NLP architectures.
• Hands-on experience with vector search algorithms, embeddings, and hybrid lexical search (TF-IDF, BM25).
• Familiarity with containerization (Docker), cloud deployment (AWS or GCP), and automated testing with PyTest.
• Solid foundation in algorithms, linear algebra, and distributed systems.`
  }
];
