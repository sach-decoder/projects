#include <iostream>      // Includes input/output stream for cin and cout
#include <algorithm>     // Includes functions like max_element and min_element

using namespace std;     // Allows use of standard namespace (e.g., cout, cin)

int main(){
    
    // Array of strings to label each day of the week
    string days[7] = {"Day1: ", "Day2: ", "Day3: ", "Day4: ", "Day5: ", "Day6: ", "Day7: "}; 
    
    // Array to store temperature values for 7 days
    int temps[7] = {}; 
    
    // Attempt to calculate array size (incorrectly uses sizeof(int) instead of sizeof(string))
    const int SIZE = sizeof(days)/sizeof(int); 
    
    int sum = 0;         // Variable to store the sum of all temperatures
    int average = 0;     // Variable to store the average temperature
    int entry = 0;       // Unused variable (can be removed)

    // Loop to input temperatures for each day
    for(int i = 0; i < 7; i++) {
        cout << "Please enter the tempreture for the day:" << endl;  // Prompt for temperature
        cout << days[i];                                             // Display current day label
        cin >> temps[i];                                             // Store input in temps array
        sum += temps[i];                                             // Add temperature to running total
    }

    // Calculate average temperature (integer division)
    average = sum / 7;

    // Display average temperature with degree symbol (char(248)) and Celsius unit
    cout << "The average tempreture for the week is: " << average << char(248) << "C" << endl;

    // Display highest temperature using max_element from <algorithm>
    cout << "The maximum for the week is: " << *max_element(temps, temps + 7) << char(248) << "C" << endl;

    // Display lowest temperature using min_element from <algorithm>
    cout << "The minimum for the week is: " << *min_element(temps, temps + 7) << char(248) << "C" << endl;

    // Loop to display all recorded temperatures in the order they were entered
    for(int j = 0; j < 7; j++){
        cout << days[j] << " " << temps[j] << char(248) << "C" << endl;  // Display day and temperature
    }

    return 0;  // End of program
}
