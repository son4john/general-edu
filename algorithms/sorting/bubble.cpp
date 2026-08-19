#include <iostream>
#include <vector>

int main(){
    int temp = 0;
    bool swapped = true;
    std::vector<int> arr = {5 ,1, 4, 3, 6, 7};
    int arrSize = arr.size();

    std::cout << "Bubble Sort Example:" << std:: endl;
    
    for(int i = 0; i < arrSize; i++){
        std::cout << arr[i] << " ";
    }
    
    std::cout << "Sorting \n";

    while(swapped){
        swapped = false;
        for(int i= 0; i < arrSize - 1; i++){
            if(arr[i] > arr[i+1]){
                temp = arr[i];
                arr[i] = arr[i+1];
                arr[i+1] = temp;
                swapped = true;
            }
        }
    }

    for(int i = 0; i < arrSize; i++){
        std::cout << arr[i] << " ";
    }

    std::cout << "Program Complete\n"; 
    return 0;
}

