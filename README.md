# Loader and Publisher in Maya with USD & ShotGrid

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This project provides a **task-based asset management system** for Maya using **Pixar USD and ShotGrid.** It streamlines the process of loading and publishing assets within a VFX pipeline, ensuring seamless integration with **ShotGrid** for task tracking and collaboration.

The system consists of two primary components:

- **Loader**: Allows artists to browse and load assigned tasks and corresponding assets.
- **Publisher**: Enables users to validate, version, and publish files to ShotGrid, notifying relevant team members.

By leveraging **USD workflows**, the tool provides a flexible and efficient way to manage assets, supporting both `.mb`/`.ma` files in Maya and referencing `.usda` files.
## Features

- **Task-Based Asset Loader** 
    - Users log in to access tasks assigned via ShotGrid
    - Task list dynamically updates upon selection
    - Displays **previous work details** along with the corresponding
    - Displays **Work** and **Published (Pub)** files
    - Double-clicking a work file loads into Maya, opening `.mb` or `.ma` while referencing `.usda`
- **Integrated Publisher**
    - Launched from the side widget in Maya
    - Users review file details and add descriptions before publishing
    - Publishes directly to **ShotGrid** and notifies relevant team members
- **Maya USD Integration**
    - Supoorts referencing **USD files (.usda)** within Maya
    - Streamlines the transition between different departments (Modeling, LookDev, Rig, Animation, Layout, Lighting, etc.)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/eval-nva5th/maya_usd
   cd maya_usd
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Install dependencies:**
    ```bash
   cd maya_usd
   chmod +x setup.sh
   ./setup.sh
   ```
- Rocky Linux / macOS
- Maya 2023 or Maya 2025
- Python 3.9
- ShotGrid API
- Flask
- Additional required libralies

3. **Set up Maya startup script**
Copy the contents of `maya_usd/publisher/server/client_server.py`  
`/maya/scripts/userSetup.py` within your MayaPath  
This ensures that the necessary server communication functions are automatically executed when Maya starts.
## Usage
### Loader
1. Open Maya and launch the **Loader** from the **shelf menu** or run this script at maya script editor
```python
import sys
import importlib
import main
sys.path.append("root directory/maya_usd/loader/")
main.show_ui()
``` 
   
2. Log in using your **username** and **email** registered in Shotgrid
3. Browse assigned tasks in loader left panel
4. Select a task a task to view :
    - **Work files** available for editing
    - **Published (Pub) files** already committed
5. **Double-click a file in the work table** to load it into Maya
    - `.mb`/`.ma` files open directly
    - **USD(.usda) files are referenced automatically**

---

### Asset Library(If you need)
1. Click the **Get assets** button in the sid widget
2. Select assets
3. Click **Load** button :
    - **USD(.usda) files are referenced automatically**

---

### Publisher
1. Click the **Publish** button in the sid widget
2. Review the version, file path, file name, and file type
3. Add a **description** (if necessary)
4. Click **Publish** :
    - Upload to **ShotGrid**
    - Notify relevant team members of the new version
5. Click **Reload** (button when receive notice):
    - Update referenced usd file

## Configuration
Add Python module path
```python
export PYTHONPATH=/YourRootDirectory/maya_usd:$PYTHONPATH
```
 


## License
**If you find this project useful, consider supporting my work:**
[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/na5_eval)

## Contact
### Project Manager
**SeungYeon Shin** - PM, Developer (Email: p2xch@example.com)  
### Team Members  
**JunSu Kim** - Developer (Email: 1115kjs@naver.com)  
**JuHye Jung** - Developer (Email: abc_49@naver.com)  
**SoonWoo Jang** - Developer (Email: f8d783@naver.com)
### Contributor
**Seonil Hong** - Advisor  
**HyungMin Park** - Advisor
