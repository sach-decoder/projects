#include <iostream>
using namespace std; 

// Function to create a new member account
void createAccount(string &name, int &memNumber, int &credits){
    cout << "-- Create Account--" << endl; 

    // Prompt user for name
    cout << "Please enter your name: "; 
    cin >> name; 

    // Prompt user for membership number
    cout << "Please enter your MemberShip Number: "; 
    cin >> memNumber; 

    // Prompt user for initial session credits
    cout << "Please enter your session credits: "; 
    cin >> credits; 

    // Validate that credits are non-negative
    if(credits < 0){
        cout << "Invalid session credits added. Must be above (1). \n"; 
        cout << "Please enter your session credits: "; 
        cin >> credits; 
    }
}

// Function to add session credits to an existing account
int addSessionCredits(int &credits, int &amountAdded){
    cout << "--Add Session Credits--" << endl; 

    // Prompt user for amount to add
    cout << "Please enter the amount of credits you would like to add: "; 
    cin >> amountAdded; 

    // Add credits to current balance
    credits += amountAdded; // Adds the entered amount to the existing credits

    // Validate that the added amount is non-negative
    if(amountAdded < 0){
        cout << "Please enter a valid session credit amount (>=0).\n"; 
        cout << "Please enter the amount of credits you would like to add: "; 
        cin >> amountAdded; 
    }
    return 0; 
}

// Function to book sessions and deduct credits
int bookSession(int &credits, int &sessionsBooked){
    cout << "--Book Session--" << endl; 
    cout << "Welcome! Thank you for wanting to book a session.\n"; 

    // Prompt user for number of sessions to book
    cout << "How many session would you like to book?: "; 
    cin >> sessionsBooked; 

    // Deduct booked sessions from available credits
    credits -= sessionsBooked; 

    // Validate that credits are still non-negative after booking
    if(credits < 0){
        cout << "Invalid credits. Please enter a valid amount of credits available.\n"; 
        cout << "How many session would you like to book?: "; 
        cin >> sessionsBooked; 
        credits -= sessionsBooked;
    }
    return 0; 
}

// Function to check remaining session credits
void checkCredits(int &credits){
    cout << "--Check Credits--" << endl; 

    // Display remaining credits if available
    if(credits > 0){
        cout << "Remaining session credits: " << credits << endl;
    } else {
        // Inform user if no credits are available
        cout << "no credits available."; 
    }
}

// Function to display account details
void displayAccountDetails(string &name, int &memNumber, int &credits){
    cout << "--Account Details--" << endl; 
    cout << "Member Name: " << name << endl; 
    cout << "Membership number: " << memNumber << endl; 
    cout << "credits avaliable: " << credits << endl; 
}

int main(){
    // Declare variables used in account management
    string name; 
    int memNumber; 
    int credits = 1; // Initial default credit
    int amountAdded = 0;
    int sessionsBooked;  

    // Declare variables for menu control
    int accountCreate; 
    int addCredit; 
    int sessionBook; 
    int creditCheck; 
    int displayDetails; 
    string exit; 
    int option; 

    // Loop to keep showing menu until user chooses to exit
    do{
        // Display main menu
        cout << "--Fitness MemberShip Managemant System--" << '\n'; 
        cout << "1. Create MemberShip Account." << '\n';     
        cout << "2. Add Session Credits" << '\n';
        cout << "3. Book a Session" << '\n';
        cout << "4. Check credits" << '\n';
        cout << "5. Display Account Details." << endl; 

        // Ask user whether to exit or continue
        cout << "Press (e) to exit, (c) to continue:"; 
        cin >> exit; 
        cout << endl; 

        // If user enters "e", loop will break.
        if(exit == "e"){
            break; 
        }
        
        // Prompt user for menu option
        cout << "Please enter a option: "; 
        cin >> option; 

        // Validate that option is within valid range
        if(option <=0 || option >5){
            cout << "Invalid input please enter a number between 1 and 5."; 
            break;  
        };

        // Execute corresponding function based on user choice
        switch(option){
            case 1: 
                createAccount(name, memNumber, credits); 
                cout << endl;
                break; 
            case 2:
                addSessionCredits(credits, amountAdded); 
                cout << endl;
                break; 
            case 3:
                bookSession(credits, sessionsBooked); 
                cout << endl;
                break; 
            case 4:
                checkCredits(credits);
                cout << endl;
                break; 
            case 5:
                displayAccountDetails(name, memNumber, credits);
                cout << endl; 
                break; 
            default:
                // Catch-all for unexpected input
                cout << "Invalid input, enter value between 1-5."; 
        }

    } while(exit != "e"); // Continue loop until user enters 'e' to exit

    return 0; 
}
