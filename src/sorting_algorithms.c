#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define MAX_SIZE 200
#define MAX_VALUE 200

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void printArray(int arr[], int n, FILE *fp) {
    for (int i = 0; i < n; i++) {
        fprintf(fp, "%d ", arr[i]);
    }
    fprintf(fp, "\n");
}

// Bubble Sort
void bubbleSort(int arr[], int n, FILE *fp) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
                printArray(arr, n, fp);
            }
        }
    }
}

// Selection Sort
void selectionSort(int arr[], int n, FILE *fp) {
    int i, j, min_idx;
    for (i = 0; i < n - 1; i++) {
        min_idx = i;
        for (j = i + 1; j < n; j++)
            if (arr[j] < arr[min_idx])
                min_idx = j;
        swap(&arr[min_idx], &arr[i]);
        printArray(arr, n, fp);
    }
}

// Insertion Sort
void insertionSort(int arr[], int n, FILE *fp) {
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
        printArray(arr, n, fp);
    }
}

// Quick Sort
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quickSortHelper(int arr[], int low, int high, FILE *fp, int n) {
    if (low < high) {
        int pi = partition(arr, low, high);
        printArray(arr, n, fp);
        quickSortHelper(arr, low, pi - 1, fp, n);
        quickSortHelper(arr, pi + 1, high, fp, n);
    }
}

void quickSort(int arr[], int n, FILE *fp) {
    quickSortHelper(arr, 0, n - 1, fp, n);
}

// Merge Sort
void merge(int arr[], int l, int m, int r, FILE *fp, int n) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;
    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
    printArray(arr, n, fp);
}

void mergeSortHelper(int arr[], int l, int r, FILE *fp, int n) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSortHelper(arr, l, m, fp, n);
        mergeSortHelper(arr, m + 1, r, fp, n);
        merge(arr, l, m, r, fp, n);
    }
}

void mergeSort(int arr[], int n, FILE *fp) {
    mergeSortHelper(arr, 0, n - 1, fp, n);
}

// Counting Sort
void countingSort(int arr[], int n, FILE *fp) {
    int output[MAX_SIZE];
    int count[MAX_VALUE + 1] = {0};
    int i;

    for (i = 0; i < n; i++)
        count[arr[i]]++;

    for (i = 1; i <= MAX_VALUE; i++)
        count[i] += count[i - 1];

    for (i = n - 1; i >= 0; i--) {
        output[count[arr[i]] - 1] = arr[i];
        count[arr[i]]--;
    }

    for (i = 0; i < n; i++) {
        arr[i] = output[i];
        printArray(arr, n, fp);
    }
}

// Radix Sort
int getMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > max)
            max = arr[i];
    return max;
}

void countSort(int arr[], int n, int exp, FILE *fp) {
    int output[n];
    int i, count[10] = {0};

    for (i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;

    for (i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }

    for (i = 0; i < n; i++) {
        arr[i] = output[i];
    }
    printArray(arr, n, fp);
}

void radixSort(int arr[], int n, FILE *fp) {
    int m = getMax(arr, n);

    for (int exp = 1; m / exp > 0; exp *= 10)
        countSort(arr, n, exp, fp);
}

// Comb Sort
void combSort(int arr[], int n, FILE *fp) {
    int gap = n;
    float shrink = 1.3;
    int sorted = 0;

    while (gap > 1 || sorted == 0) {
        gap = (int)(gap / shrink);
        if (gap < 1)
            gap = 1;

        sorted = 1;
        for (int i = 0; i + gap < n; i++) {
            if (arr[i] > arr[i + gap]) {
                swap(&arr[i], &arr[i + gap]);
                sorted = 0;
                printArray(arr, n, fp);
            }
        }
    }
}

void generateRandomArray(int arr[], int n) {
    for (int i = 0; i < n; i++)
        arr[i] = rand() % MAX_VALUE;
}

void runSortingAlgorithm(const char* name, void (*sortFunc)(int[], int, FILE*), int arr[], int n) {
    int temp[MAX_SIZE];
    memcpy(temp, arr, n * sizeof(int));

    char filename[50];
    sprintf(filename, "%s_output.txt", name);
    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        printf("Error opening file %s\n", filename);
        return;
    }

    printf("Generated Array: ");
    printArray(temp, n, stdout); // Print to CMD
    // printf("\n");

    printf("Running %s...\n", name);
    printArray(temp, n, fp); // Initial array printed to file

    printf("Sorting in progress...\n");
    sortFunc(temp, n, fp); // Sort and write steps to file

    printf("Sorted Array: ");
    printArray(temp, n, stdout); // Print sorted array to CMD
    printf("\n");
    printf("Sorting steps written to %s successfully.\n\n", filename);
    fclose(fp);
}

int main() {
    srand(time(NULL));
    int arr[MAX_SIZE];
    int n = 100; // Change this to adjust the size of the array

    generateRandomArray(arr, n);

    runSortingAlgorithm("bubblesort", bubbleSort, arr, n);
    runSortingAlgorithm("selectionsort", selectionSort, arr, n);
    runSortingAlgorithm("insertionsort", insertionSort, arr, n);
    runSortingAlgorithm("quicksort", quickSort, arr, n);
    runSortingAlgorithm("mergesort", mergeSort, arr, n);
    runSortingAlgorithm("countingsort", countingSort, arr, n);
    runSortingAlgorithm("radixsort", radixSort, arr, n);
    runSortingAlgorithm("combsort", combSort, arr, n);

    return 0;
}