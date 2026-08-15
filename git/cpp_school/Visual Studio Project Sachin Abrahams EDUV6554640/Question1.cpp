#include <iostream>
#include <iomanip>
#include <string>

using namespace std;

const int MAX_ITEMS = 10;
const int CATALOG_SIZE = 8;
const double DISCOUNT_THRESHOLD = 2000.0;
const double DISCOUNT_RATE = 0.15;

// Gadget names and prices
string gadgetNames[CATALOG_SIZE] = {
    "Wireless Mouse", "Bluetooth Speaker", "USB Flash Drive", "Gaming Keyboard",
    "Noise-Cancelling Headphones", "Smartwatch", "External Hard Drive", "Portable Charger"
};

double gadgetPrices[CATALOG_SIZE] = {
    150.0, 250.0, 100.0, 500.0, 750.0, 1200.0, 1000.0, 300.0
};

void displayCatalogue() {
    cout << "\nGadget Catalogue:\n";
    for (int i = 0; i < CATALOG_SIZE; ++i) {
        cout << "  " << (i + 1) << ". " << gadgetNames[i]
             << " - R" << fixed << setprecision(2) << gadgetPrices[i] << endl;
    }
}

int main() {
    string firstName, lastName;
    int itemNumbers[MAX_ITEMS], quantities[MAX_ITEMS];
    double subtotal = 0.0;

    // Prompt user details
    cout << "Enter your first name: ";
    cin >> firstName;
    cout << "Enter your last name: ";
    cin >> lastName;

    // Display catalogue
    displayCatalogue();

    cout << "\n Select up to 10 items by entering item number and quantity.\n";

    for (int i = 0; i < MAX_ITEMS; ++i) {
        int itemNum, qty;

        cout << "\nItem " << (i + 1) << " - Enter item number (1-8, or 0 to stop): ";
        cin >> itemNum;

        if (itemNum == 0) break;

        // Validate item number
        while (itemNum < 1 || itemNum > CATALOG_SIZE) {
            cout << " Invalid item number. Please enter a number between 1 and 8: ";
            cin >> itemNum;
        }

        cout << "Enter quantity: ";
        cin >> qty;

        // Validate quantity
        while (qty < 1) {
            cout << " Quantity must be at least 1. Try again: ";
            cin >> qty;
        }

        itemNumbers[i] = itemNum;
        quantities[i] = qty;

        subtotal += gadgetPrices[itemNum - 1] * qty;
    }

    // Apply discount if applicable
    double discount = 0.0;
    if (subtotal > DISCOUNT_THRESHOLD) {
        discount = subtotal * DISCOUNT_RATE;
    }

    double finalTotal = subtotal - discount;

    // Display results
    cout << "\n Purchase Summary for " << firstName << " " << lastName << ":\n";
    cout << "----------------------------------------\n";
    cout << "Subtotal:         R" << fixed << setprecision(2) << subtotal << endl;
    cout << "Discount Applied: R" << discount << endl;
    cout << "Final Total:      R" << finalTotal << endl;
    cout << "----------------------------------------\n";

    return 0;
}
