# Automated CI/CD Project with GitOps – Jira Automation Dashboard

## Project Overview

This project demonstrates a complete **CI/CD and GitOps pipeline** for a containerized **FastAPI** application that visualizes a **Jira dashboard**.

On every commit to GitHub, a CI pipeline is triggered to:

- validate the application code,

- build a Docker image,

- push the image to Docker Hub,

- update Kubernetes manifests stored in Git.

Using **GitOps principles**, **Argo CD** continuously monitors the repository and automatically synchronizes and deploys the application to a **Kubernetes cluster** whenever changes are detected.

The application exposes **health** and **metrics** endpoints, making it suitable for **production-ready deployment and observability**.

---

## Repository Structure

```
.
├── app/                      # FastAPI application
│   ├── main.py               # API, UI, health & metrics endpoints
│   ├── metrics.py            # Prometheus metrics definitions
│   └── templates/
│       └── index.html        # Jira dashboard UI
├── tests/                    # Unit tests
├── requirements.txt
├── Dockerfile                # Containerization
├── .github/workflows/
│   └── ci-cd.yaml            # CI/CD pipeline definition
├── ops/
│   ├── k8s/                  # Kubernetes manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── servicemonitor.yaml
│   │   └── kustomization.yaml
│   └── argocd/
│       └── application.yaml  # Argo CD GitOps application
└── README.md
```

---

## Solution Design

The solution follows a **T-shaped DevOps approach**.

### Breadth

The project covers the full delivery lifecycle:

* Source control with Git
* Continuous Integration
* Container image build and scanning
* GitOps-based Continuous Deployment
* Kubernetes runtime
* Metrics and observability

### Depth

Deeper focus is placed on **GitOps and immutable deployments**:

* Git used as the primary deployment reference
* Kubernetes manifests updated automatically from CI
* Argo CD reconciliation loop for desired state enforcement
* Docker images versioned by Git commit SHA

---

## Application

The application is a **FastAPI-based Jira Automation Dashboard**.

It integrates with **Jira Cloud** and visualizes recent work items in a simple web UI, including:

* Issue summary
* Work type (issue type) with icon
* Status
* Assignee

The service exposes:

* a basic web UI
* a `/health` endpoint for Kubernetes probes
* a `/metrics` endpoint exposing Prometheus-compatible metrics

---

## Continuous Deployment with GitOps

Deployment is handled using **Argo CD**:

* Git defines the desired Kubernetes state
* Argo CD watches the repository
* Manifest changes are applied automatically to the cluster

Argo CD is the only component that deploys to Kubernetes, enforcing a strict GitOps model.

---

## Kubernetes Runtime

The application runs as a Kubernetes Deployment:

* Multiple replicas demonstrate availability
* A Service load-balances traffic
* Rolling updates provide zero-downtime deployments


---

## Observability

Basic observability is implemented via Prometheus-compatible metrics exposed at `/metrics`.

Collected metrics include:

* HTTP request counts
* Request latency histograms
* Application version and environment metadata


---

## Scope and Limitations

To keep the project focused and easy to demonstrate, the following were intentionally left out:

* Multiple environments - dev, staging, production
* Alerting based on monitoring tools such as Grafana
* Advanced secret management solutions


---

## Summary

This project demonstrates:

* an automated CI/CD pipeline
* immutable container images versioned by Git SHA
* GitOps-based deployment with Argo CD
* Kubernetes-based application runtime
* basic but effective observability

