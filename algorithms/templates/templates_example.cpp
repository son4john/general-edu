#include <iostream>
#include <string>

// 1. Function template: works for any type that supports operator>
template <typename T>
T maxOf(T a, T b) {
    return (a > b) ? a : b;
}

// 2. Class template: a simple generic box that holds one value
template <typename T>
class Box {
public:
    Box(T value) : value_(value) {}

    T get() const { return value_; }
    void set(T value) { value_ = value; }

private:
    T value_;
};

// 3. Template specialization: custom behavior for Box<std::string>
template <>
class Box<std::string> {
public:
    Box(std::string value) : value_(value) {}

    std::string get() const { return "\"" + value_ + "\""; } // quote strings

private:
    std::string value_;
};

// 4. Template with multiple type parameters
template <typename A, typename B>
void printPair(A a, B b) {
    std::cout << "(" << a << ", " << b << ")\n";
}

int main() {
    // Function template usage — compiler infers T for each call
    std::cout << "maxOf(3, 7)       = " << maxOf(3, 7) << "\n";
    std::cout << "maxOf(3.5, 2.1)   = " << maxOf(3.5, 2.1) << "\n";
    std::cout << "maxOf('a', 'z')   = " << maxOf('a', 'z') << "\n";

    // Class template usage
    Box<int> intBox(42);
    Box<double> doubleBox(3.14);
    std::cout << "intBox.get()      = " << intBox.get() << "\n";
    std::cout << "doubleBox.get()   = " << doubleBox.get() << "\n";

    // Specialized class template
    Box<std::string> strBox("hello templates");
    std::cout << "strBox.get()      = " << strBox.get() << "\n";

    // Multi-parameter template
    printPair(1, "one");
    printPair(2.5, 'x');

    return 0;
}
