#include <iostream>

// Case A: templated INPUT, fixed OUTPUT type
// T can be anything that supports %, but we always return bool.
template <typename T>
bool isEven(T value) {
    return value % 2 == 0;
}

// Case B: fixed INPUT type, templated OUTPUT
// The argument is always a float, but T decides what we cast it to.
template <typename T>
T fromFloat(float value) {
    return static_cast<T>(value);
}

int main() {
    // Case A: T is inferred from the argument, as usual.
    std::cout << "isEven(4)   = " << isEven(4) << "\n";
    std::cout << "isEven(7)   = " << isEven(7) << "\n";
    std::cout << "isEven(10L) = " << isEven(10L) << "\n"; // T = long here

    // Case B: T can't be inferred from a float argument alone,
    // so we must tell the compiler explicitly with <...>.
    int   asInt   = fromFloat<int>(3.9f);
    char  asChar  = fromFloat<char>(65.0f);
    double asDbl  = fromFloat<double>(2.5f);

    std::cout << "fromFloat<int>(3.9f)    = " << asInt << "\n";
    std::cout << "fromFloat<char>(65.0f)  = " << asChar << "\n";
    std::cout << "fromFloat<double>(2.5f) = " << asDbl << "\n";

    return 0;
}
