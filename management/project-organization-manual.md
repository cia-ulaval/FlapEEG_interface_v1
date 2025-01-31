# Flappy EEG - winter 2025 - Project Organization Manual

---

# Table of Contents
1. [Introduction](#1-introduction)
   - [Project Name](#1-introduction)
   - [Prepared by](#1-introduction)
   - [Approved by](#1-introduction)
   - [Purpose](#1-introduction)

2. [Project Overview](#2-project-overview)
   - [Objectives](#21-objectives)
   - [Scope](#22-scope)
   - [Deliverables](#23-deliverables)

3. [Project Team and Roles](#3-project-team-and-roles)
   - [Organization Chart](#31-organization-chart)
   - [Roles and Responsibilities](#32-roles-and-responsibilities)
   - [Contact Information](#33-contact-information)

4. [Processes and Procedures](#4-processes-and-procedures)
   - [Project Phases](#41-project-phases)
   - [Communication Plan](#42-communication-plan)

5. [Tools and Resources](#5-tools-and-resources)
   - [Software and Tools](#51-software-and-tools)
   - [Templates and Documentation](#52-templates-and-documentation)

6. [Change Management](#6-change-management)
   - [Change Request Process](#61-change-request-process)
   - [Version Control](#62-version-control)

7. [Schedule and Milestones](#7-schedule-and-milestones)

8. [Budget and Resources](#8-budget-and-resources)

9. [Closing Procedures](#9-closing-procedures)
    - [Archiving Documentation](#9-closing-procedures)
    - [Final Report](#9-closing-procedures)
    - [Lessons Learned](#9-closing-procedures)

10. [Appendices](#10-appendices)
    - [Glossary of Terms](#10-appendices)
    - [Reference Documents](#10-appendices)
    - [Other Supporting Materials](#10-appendices)

---

## 1. Introduction
- **Project Name**: Flappy EEG
- **Prepared by**: Louis-Etienne Messier
- **Approved by**:  
- **Purpose**:  
  Plans out and describes the management procedure for this project. You can refer to this document for insights about the project.

---

## 2. Project Overview
### 2.1 Objectives
#### Primary objectives of the project
- Give student a research to practical experience
- Create a group project from scratch
- Have a functional prototype that allows a user to play a game with it's EEG signal
- Learn how to do Teamwork
- Develop research and programming skills  

### 2.2 Scope
#### Define what is included and excluded in the project scope
- Develop a prototype
- Weekly work meetings on monday - maybe another day
- Programming-pizza days
- Research reading
- Generate dataset
- Filtering signals
- Programming EEG API 
- Training a small model

### 2.3 Deliverables
#### List the key deliverables for the project
1. Functional EEG helmet
2. Open-BCI interface setup and tested with the helmet
3. A python script connected to Open-BCI interface
4. Baseline eye signal makes bird jump
5. Protocol for data acquisition (python app to record data)
6. Data acquisition (go to Vachon with a stand)
7. Signal treatment
8. AI Model -> Pytorch
9. Train AI model -> Pytorch on a GPU (with parrallism)
10. Integrate game with model

---

## 3. Project Team and Roles
### 3.1 Organization Chart
- Include a diagram of the project's organizational structure (can reference an external file or provide ASCII art).  

### 3.2 Roles and Responsibilities
| Role               | Name                | Responsibilities                        |
|--------------------|---------------------|-----------------------------------------|
| Project Manager    | Louis-Etienne Messier             | Overall planning, execution, and reporting | 
| Team Member 1      | Jordan Mathieu                    | Specific tasks and responsibilities      | 
| Team Member 2      |                     | Specific tasks and responsibilities      |

### 3.3 Contact Information
| Name               | Role               | Email              | Phone             |
|--------------------|--------------------|--------------------|-------------------|
| Louis-Etienne Messier             |      Project Manager               |        lemes3@ulaval.ca            |             438-295-9256      |
| Jordan Mathieu | Team Member 1 | jordan.mathieu.2@ulaval.ca  | 418-637-8501 | 
| Amen Ouannes | Team Member 2 | amoua17@ulaval.ca  | 581-459-2206 | 
| William Blanchet Lafrenière | Team Member 3 | wibll@ulaval.ca | 581-997-7927 | 
| Estelle Tournassat | Team Member 4 | estou4@ulaval.ca | 581-988-9849 | 
| Dereck Bélanger | Team Member 5 | derekblanger@gmail.com | 581-308-6181 | 
| Hedi Braham | Team Member 6 | mhbra5@ulaval.ca | 418-262-4406 |

---

## 4. Processes and Procedures
### 4.1 Project Phases
1. **Initiation**
- Team member recruitement
- Kick-off meeting
- Arrange a time zone for working
2. **Planning**  
- Gantt Chart
- Task assignment
- Some research

3. **Execution**  
- Functional EEG helmet
- Open-BCI interface setup and tested with the helmet
- A python script connected to Open-BCI interface
- Baseline eye signal makes bird jump
- Protocol for data acquisition (python app to record data)
- Data acquisition (go to Vachon with a stand)
- Signal treatment
- AI Model -> Pytorch
- Train AI model -> Pytorch on a GPU (with parrallism)
- Integrate game with model

4. **Monitoring & Controlling**  
 - Every deliverable is documented in a markdown file or a Jupyter notebook, with pictures and description of what was done
 - Follow the Gantt Chart for the project duration
 - Weekly mandatory 1h meeting (CA du projet) + 3h of work per week
5. **Closure**  
 - Post-mortem

### 4.2 Communication Plan
- Weekly mandatory 1h meeting in person : VCH-00087
- Discord is the central repository of team communication

---

## 5. Tools and Resources
### 5.1 Software and Tools
| Tool              | Purpose               | Access Details        |
|-------------------|-----------------------|-----------------------|
| Python           | Programming language       | https://www.python.org/  |
| Discord            | Communication         | https://discord.com/ |
| Markdown |   Documentation | Create it with a text editor and add it to the Github repo | 
| Jupyter notebook | Documentation | Create it with a text editor and add it to the Github repo | 
| Github | Programming project sharing | https://github.com/ | 

### 5.2 Templates and Documentation
- To document project advances, create a .md file or a Jupyter notebook with code snippets
- A good template is : https://github.com/cia-ulaval/EEG_Interface/blob/feature/feature-extraction/notebooks/eeg_prediction.ipynb

---

## 6. Change Management
### 6.1 Change Request Process
#### Describe the process for requesting, reviewing, and approving changes
- This project is a small community project, so no need for approval for small changes. Anything consequential should be brought up in the weekly team meeting to be voted on. If majority approves, it's accepted. If a tie, it's rejected.   

### 6.2 Version Control
#### Tools and methods for version control (e.g., Git, shared documents)
- Use github, with your own dev branch, and make PR's that have to be accepted to be merged on the main. 

---

## 7. Schedule and Milestones

**See the GitHub Flappy EEG Project to follow the deadlines**

https://github.com/orgs/cia-ulaval/projects/7

---

## 8. Budget and Resources
- Temporal ressources : 11 weeks
- Manpower : 5 people - 3h min = 15h per week
- Monetary : flexible
---

## 9. Closing Procedures
- Archiving project documentation
- Post-mortem 

---

## 10. Appendices 

---

**End of Document**

<br>

# Signatures
By signing here you consent to oblige by the guidelines outlined in this document. In short, you will have to :
1. Attend the weekly 1h meeting
2. Dedicate at least 3h or every week working on the project
3. Have fun!

---
- Louis-Etienne Messier : :white_check_mark:
- Jordan Mathieu : :white_check_mark: