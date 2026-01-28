# Automated CI/CD Project with GitOps – Jira Automation Dashboard

## Overview

This repository demonstrates a **compact but complete CI/CD and GitOps workflow** for a containerized backend application deployed to Kubernetes.

The main goal is to illustrate how a change flows from **Git commit → CI validation → container build → GitOps-based deployment → runtime observability**, without any manual deployment steps.

The project intentionally keeps application logic lightweight so the focus stays on **delivery automation, traceability, and operational correctness**.

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
├── Dockerfile
├── .github/workflows/
│   └── ci-cd.yaml            # CI/CD pipeline definition
├── ops/
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── servicemonitor.yaml
│   │   ├── ingress.yaml      # Optional (cluster-dependent)
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

* Git as the single source of truth
* Kubernetes manifests updated automatically from CI
* Argo CD reconciliation
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

## CI/CD Pipeline

The CI/CD pipeline is implemented with **GitHub Actions** and runs on the `main` branch.

### CI responsibilities

* Run linting and unit tests
* Build a Docker image
* Scan the image for vulnerabilities
* Push the image to a container registry
* Update Kubernetes manifests with the new image tag

Images are tagged with the **Git commit SHA**, ensuring immutability and traceability.

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

Local access is provided via **NodePort** (Ingress is optional, depending on the cluster).

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
* ChatOps for nottifications
* Alerting based on monitoring tools (Grafana)
* Advanced secret management solutions


---

## Summary

This project demonstrates:

* an automated CI/CD pipeline
* immutable container images versioned by Git SHA
* GitOps-based deployment with Argo CD
* Kubernetes-based application runtime
* basic but effective observability

The result is a **clean, reproducible, and fully automated delivery workflow** 
