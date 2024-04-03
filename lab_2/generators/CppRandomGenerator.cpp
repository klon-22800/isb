#include <iostream>
#include <random>

using namespace std;

int random(int a, int b) {
		random_device random_device;
		mt19937 generator(random_device());
		uniform_int_distribution<> distribution(a, b);
		return distribution(generator);
}

void random_generator(int number_bits){
    for(int i = 0; i< number_bits; i++){
        cout<<random(0,1);
    }
}

int main() {
    const int NUMBER_BITS = 128;
    random_generator(NUMBER_BITS);
    return 0;
}