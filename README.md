# PayCrypt

## Overview

- PayCrypt was an AI-based hackathon hosted by NPCI, where one of the probelm statements were to streamline toll plaza movements, while collecting data for further analysis.
Our solution included data analysis in the form of graphs of the traffic movement in multiple regions of Bangalore, while developing an algorithm to optimize toll plaza operations, by suggesting which lane to choose to the upcoming cars where least amount of time would be taken.
- Each different type of vehicle was given a value (for example - `car value = 0.75`), and a final score was calculated by the algorithm comparing the total value in each lane, the one with the least would be suggested to the approaching driver.
- Along with this, an algorithm was also made to calculate fines related to trucks carrying more weight than the allowed official amount by the government, calculation was done via sensors installed near the tolls in the plaza, to calculate tyre pressure, an compare it with the average tyre pressure for the vehicle identified by AI.


## Repository Structure

- **Merchant/**: Contains code related to merchant-side operations, including handling transactions and managing accounts.
- **Bangalore_1Day_NETC.csv**: A CSV file that may contain sample data or transaction records for testing.
- **requirements.txt**: Lists the Python dependencies required to run the project.

## Getting Started

To set up and run the PayCrypt project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/prakhar175/PayCrypt.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd PayCrypt
   ```

3. **Install Dependencies**:
   Ensure you have Python installed on your system, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Project**:
   - Explore the contents of the `Merchant` directory.
   - Execute relevant scripts to test the functionality.

## Contributors:
   - Prakhar Kothari
   - Shreeyans Arora
   - Mohit Bhalotia
   - Sumeet Kumar
   - Naresh
   

## Contributing

Contributions are welcome! If you'd like to contribute:
- Fork the repository.
- Create a new branch for your feature.
- Submit a pull request with detailed explanations of your changes.

## License

This project does not specify a license. For any inquiries regarding usage and contributions, please contact the repository owner at [Prakhar Kothari](https://github.com/prakhar175), [Shreeyans Arora](https://github.com/shreeyans2808), [Mohit Bhalotia](https://github.com/MohitBhalotia) or [Sumeet Kumar](https://github.com/SumeetKumarr).
