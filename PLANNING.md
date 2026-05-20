# Task Manager — Project Planning Document

## Objective
Deploy a full-stack CRUD Task Manager application on AWS EC2
using Python and Flask, with an automated CI/CD pipeline
via GitHub Actions.

## Tech Stack
- Language:    Python 3.x
- Framework:   Flask (lightweight Python web framework)
- Database:    SQLite (Python built-in — no extra AWS service needed)
- Hosting:     AWS EC2 t2.micro (free tier eligible)
- CI/CD:       GitHub Actions
- Process Mgr: PM2 (manages Python process on server)
- Version Ctrl: Git + GitHub

## Architecture Flow
Local Dev → GitHub Push → GitHub Actions (CI/CD) → AWS EC2 → Live App

## AWS Services Used
1. EC2 (Elastic Compute Cloud) — t2.micro, Ubuntu 22.04 LTS
2. IAM (Identity and Access Management) — EC2 role, least-privilege
3. Security Groups — Firewall / inbound traffic rules for EC2

## Security Measures
- EC2 Security Group: only ports 22 (SSH) and 3000 (app) open
- IAM Role attached to EC2 — no hardcoded AWS credentials anywhere
- SSH Private Key stored as GitHub Encrypted Secret (never in code)
- .gitignore prevents accidental commit of keys, DB, env files
- Non-root ubuntu user with sudo only

## CI/CD Pipeline Steps
1. Developer pushes code to main branch on GitHub
2. GitHub Actions workflow is triggered automatically
3. Pipeline installs Python dependencies and runs a syntax check
4. On success, SSH into EC2, pull latest code, reinstall deps, restart app
5. App is live at http://[EC2-PUBLIC-IP]:3000

## Free Tier Cost Estimate
- EC2 t2.micro:   750 hrs/month FREE (using ~24 hrs for demo)
- Data Transfer:  1 GB/month FREE
- IAM, SGs:       always FREE
- Estimated cost: ₹0.00

## CRUD Operations
- CREATE : POST   /api/tasks        — add a new task
- READ   : GET    /api/tasks        — fetch all tasks
- UPDATE : PUT    /api/tasks/<id>   — mark task done/pending
- DELETE : DELETE /api/tasks/<id>  — remove a task