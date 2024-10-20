<a id="readme-top"></a>
<h3 align="center">Genshin Impact Artifact Optimisation Simulator</h3>

  <p align="center">
    A Python tool for optimising Genshin Impact character builds by calculating maximum theoretical damage and simulating artifact domain farming to evaluate marginal damage gains, helping players determine when to shift investment between characters
    <br />
    <br />
    <a href="https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#running-the-project">Running the Project</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#simulation-stages">Simulation Stages</a></li>
        <li><a href="#important-assumptions">Important Assumptions</a></li>
        <li><a href="#visualisation-examples">Visualisation Examples</a></li>
      </ul>
    </li>
    <li><a href="#code-structure">Code Structure</a></li>
    <li><a href="#future-improvements">Future Improvements</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#sources-and-inspiration">Sources and Inspiration</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is designed to help Genshin Impact players optimise their characters by calculating the maximum theoretical damage for a given character and weapon combination, as well as simulating artifact domain farming to find the marginal damage increases for different stages of builds.
The tool is especially useful for free-to-play (F2P) players who need to manage their limited resources wisely. By analysing damage potential and farming efficiency, you can find how close your build is to its maximum potential and decide when it's better to shift focus from one character to another for optimal progression.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Before running the project ensure that you have installed Python 3.x and the following packages: 
* Numpy
* Matplotlib

You can install them via pip:
  ```sh
  pip install numpy matplotlib
  ```
Alternatively, you can install **Anaconda** which includes these libraries by default: [Download Anaconda](https://www.anaconda.com/download)

### Running the Project

1. Clone the repository
   ```sh
   git clone https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator.git
   cd Artifact-Optimization-Simulator
   ```
2. Run the simulation

&emsp; &ensp; Simply open the `main.py` file in your preferred code editor or IDE, and click **Run** to start the simulation.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After starting the program, you will be prompted to input the **character name**, **weapon**, **artifact set**, and **elemental reaction**.

Supported options:
- **Characters**: Tartaglia, Xiangling
- **Weapons**: Skyward Harp, The Catch
- **Artifact Set**: Heart of Depth, Emblem of Severed Fate
- **Reaction**: Vaporise, Reverse Vaporise, Melt, Reverse Melt

### Simulation Stages

1. **Theoretical Maximum Damage**  
   The programme will compute the optimal artifact combination based on user input. The result is displayed as a full character build with details about substat distributions, total final stats, and the highest damage loadout.
   
   **Output:**
   - Best substat combinations for each artifact piece (flower, feather, sands, goblet, circlet)
   - The final character stats (including base-stats)
   - The total damage
   - How many unique alternative builds achieve the same damage

3. **Monte Carlo Simulation of Artifact Domain Farming**  
   The simulation replicates the process of farming an artifact domain, taking into account probabilities for drop rates, set pieces, substats, and other randomness. Each run simulates 1,350 domain completions (roughly 5 months of farming) to estimate marginal damage improvements over time.
   
   **Output:**
   - A plot of damage progression for each simulation
   - A final plot showing the average damage and a 95% confidence interval
   - Moving average percentage growth rate to suggest optimal stopping points
  
   For example, if you choose to run 50 simulations, the programme will simulate 1,350 domain runs for each simulation. You'll see the progress as it completes each simulation (including the maximum damage reached), and the final plot will show both individual simulation results and the overall trend.

### Important Assumptions 
- Characters are assumed to be at **level 80** with their final ascension
- Enemy level is set to **92** with **10% resistance**
- The programme does **not account for off-pieces** (artifacts from other sets), which are common in real builds for flexibility
- **Artifact recycling** (Strongbox) is not considered in the simulation

### Visualisation Examples

gif of running code

Example plots with confidence intervals

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- STRUCTURE -->
## Code Structure

This project is organised into several Python modules, each handling different aspects of the artifact optimisation and simulation process. Below is a brief overview of each file:
- `main.py`:
  This is the main script that orchestrates the entire process. It handles user input, initiates both the theoretical maximum damage calculation and the artifact farming simulation, and generates the output plots.

- `artifactclasses.py`:
  Contains the classes and data structures for artifacts and loadouts. This file defines how artifacts are represented, including main stats, sub stats, and how they combine to form a character's complete loadout.
- `artifactcombos.py`:
  Generates all possible artifact stat combinations used for calculating the maximum theoretical damage. This module creates combinations based on the predefined sets of stats and filters.
- `characterselection.py`:
  Manages character information and user input. It contains predefined data for each character, such as their base stats, weapons and elemental reactions. This module also prompts the user to select a character, weapon, artifact set, and reaction type.
- `damagecalculator.py`:
  Computes damage for specific substat combinations. This module calculates the expected damage output based on the stats provided for the artifact set, character, weapon, and elemental reaction.
- `damagecalculator_v2.py`:
  A refined version of the original damage calculator that works specifically for randomly generated artifacts. It expands on the initial version to support the Monte Carlo simulation but will eventually need further adaption t ohandle characters that scale with different stats.
- `montecarlosim.py`:
  Contains the Monte Carlo simulation logic for artifact farming. This module simulates multiple independent farming sessions, recording the damage improvements over time and providing data for plotting the overall progression.
- `pruningtools.py`:
  A set of helper functions used to prune the list of potential artifact combinations. These tools help reduce the number of artifact sets under consideration by filtering out combinations that don't meet certain criteria, improving the efficicency of the maximum damage calculation.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Future Improvements

- Add support for more characters and weapons
- Optimise code to reduce reduncancy and improve efficiency
- Support characters that don't scale off attack or crit
- Add a graphical user interface (GUI) for easier input and better user experience

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Suggestions and improvements are welcome!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Joshua Rudloff - jrudloff2015@gmail.com

Project Link: [https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator](https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Sources and Inspiration

* Inspired by the tool at [IWinToLose](iwintolose.com), which focuses on average roll values but doesn't consider the absolute maximum damage
* Genshin Impact Theory
  * [Genshin Impact Wiki](https://genshin-impact.fandom.com/wiki/)
  * [Keqing Mains Wiki](https://keqingmains.com/misc/artifacts/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Josh-Rudloff/Artifact-Optimisation-Simulator.svg?style=for-the-badge
[contributors-url]: https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Josh-Rudloff/Artifact-Optimisation-Simulator.svg?style=for-the-badge
[forks-url]: https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator/network/members
[stars-shield]: https://img.shields.io/github/stars/Josh-Rudloff/Artifact-Optimisation-Simulator.svg?style=for-the-badge
[stars-url]: https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator/stargazers
[issues-shield]: https://img.shields.io/github/issues/Josh-Rudloff/Artifact-Optimisation-Simulator.svg?style=for-the-badge
[issues-url]: https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator/issues
[license-shield]: https://img.shields.io/github/license/Josh-Rudloff/Artifact-Optimisation-Simulator.svg?style=for-the-badge
[license-url]: https://github.com/Josh-Rudloff/Artifact-Optimisation-Simulator/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
