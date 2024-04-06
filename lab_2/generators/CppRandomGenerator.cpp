#include <iostream>
#include <random>

using namespace std;

/*!
  @brief the function will return a random integer in the range from a to b
  @param a, b generation gap
  @return random integer in the range from a to b
 */
int random(int a, int b) {
		random_device random_device;
		mt19937 generator(random_device());
		uniform_int_distribution<> distribution(a, b);
		return distribution(generator);
}
/*!
  @brief the function outputs a pseudo-random bit sequence
  @param number_bits sequence length
 */
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