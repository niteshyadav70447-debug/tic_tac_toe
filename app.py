
import streamlit as st
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(
    page_title="DAA Sorting Visualizer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sorting Algorithm Visualizer")
st.subheader("Design and Analysis of Algorithms (DAA)")

st.write(
    "Visualize how different sorting algorithms "
    "arrange numbers in ascending order."
)

# Algorithm information
algorithms = {
    "Bubble Sort": {
        "best": "O(n)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)"
    },
    "Selection Sort": {
        "best": "O(n²)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)"
    },
    "Insertion Sort": {
        "best": "O(n)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)"
    },
    "Merge Sort": {
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n log n)",
        "space": "O(n)"
    },
    "Quick Sort": {
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n²)",
        "space": "O(log n) average"
    }
}

# Sorting event generator
def sorting_steps(arr, algorithm):

    a = arr.copy()
    events = []
    comparisons = 0
    swaps = 0

    def save(i=-1, j=-1):
        events.append(
            (a.copy(), i, j, comparisons, swaps)
        )

    if algorithm == "Bubble Sort":

        n = len(a)

        for i in range(n):
            for j in range(n - i - 1):
                comparisons += 1

                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swaps += 1

                save(j, j + 1)

    elif algorithm == "Selection Sort":

        n = len(a)

        for i in range(n):
            minimum = i

            for j in range(i + 1, n):
                comparisons += 1

                if a[j] < a[minimum]:
                    minimum = j

                save(j, minimum)

            if minimum != i:
                a[i], a[minimum] = a[minimum], a[i]
                swaps += 1

            save(i, minimum)

    elif algorithm == "Insertion Sort":

        for i in range(1, len(a)):
            key = a[i]
            j = i - 1

            while j >= 0:
                comparisons += 1

                if a[j] > key:
                    a[j + 1] = a[j]
                    swaps += 1
                    save(j, j + 1)
                    j -= 1
                else:
                    save(j, i)
                    break

            a[j + 1] = key
            save(j + 1, i)

    elif algorithm == "Merge Sort":

        def merge_sort(left, right):

            nonlocal comparisons, swaps

            if left >= right:
                return

            mid = (left + right) // 2

            merge_sort(left, mid)
            merge_sort(mid + 1, right)

            L = a[left:mid + 1]
            R = a[mid + 1:right + 1]

            i = j = 0
            k = left

            while i < len(L) and j < len(R):
                comparisons += 1

                if L[i] <= R[j]:
                    a[k] = L[i]
                    i += 1
                else:
                    a[k] = R[j]
                    j += 1

                swaps += 1
                save(k, k)
                k += 1

            while i < len(L):
                a[k] = L[i]
                i += 1
                k += 1
                swaps += 1
                save(k - 1, k - 1)

            while j < len(R):
                a[k] = R[j]
                j += 1
                k += 1
                swaps += 1
                save(k - 1, k - 1)

        merge_sort(0, len(a) - 1)

    elif algorithm == "Quick Sort":

        def quick_sort(low, high):

            nonlocal comparisons, swaps

            if low < high:

                pivot = a[high]
                i = low - 1

                for j in range(low, high):
                    comparisons += 1

                    if a[j] <= pivot:
                        i += 1

                        if i != j:
                            a[i], a[j] = a[j], a[i]
                            swaps += 1

                        save(i, j)
                    else:
                        save(j, high)

                if i + 1 != high:
                    a[i + 1], a[high] = a[high], a[i + 1]
                    swaps += 1

                save(i + 1, high)

                p = i + 1

                quick_sort(low, p - 1)
                quick_sort(p + 1, high)

        quick_sort(0, len(a) - 1)

    save()
    return events


# Sidebar
st.sidebar.header("⚙️ Settings")

algorithm = st.sidebar.selectbox(
    "Select Algorithm",
    list(algorithms.keys())
)

size = st.sidebar.slider(
    "Number of Elements",
    5, 30, 15
)

speed = st.sidebar.slider(
    "Animation Speed",
    0.01, 0.5, 0.10
)

input_mode = st.sidebar.radio(
    "Input Type",
    ["Random Numbers", "Custom Numbers"]
)

if input_mode == "Custom Numbers":
    custom_input = st.sidebar.text_input(
        "Enter numbers separated by commas",
        "45, 12, 78, 23, 56, 9"
    )

    try:
        original = [
            int(x.strip())
            for x in custom_input.split(",")
        ]

        if not original or len(original) > 30:
            st.sidebar.error("Enter 1 to 30 numbers.")
            original = [45, 12, 78, 23, 56, 9]

    except ValueError:
        st.sidebar.error("Please enter valid numbers.")
        original = [45, 12, 78, 23, 56, 9]

else:
    original = [
        random.randint(5, 100)
        for _ in range(size)
    ]

if st.sidebar.button("🔀 Generate New Array"):
    st.rerun()

# Complexity section
info = algorithms[algorithm]

st.markdown("### 📚 Algorithm Complexity")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Best Case", info["best"])
c2.metric("Average Case", info["average"])
c3.metric("Worst Case", info["worst"])
c4.metric("Space", info["space"])

st.divider()

st.markdown("### 📊 Sorting Visualization")

st.write("Selected Algorithm:", algorithm)

chart_area = st.empty()
stats_area = st.empty()
status_area = st.empty()

def draw_chart(values, x=-1, y=-1):

    fig, ax = plt.subplots(figsize=(11, 4))

    colors = [
        "orange" if i == x or i == y else "skyblue"
        for i in range(len(values))
    ]

    ax.bar(range(len(values)), values, color=colors)

    ax.set_xlabel("Array Index")
    ax.set_ylabel("Value")
    ax.set_title(algorithm)

    ax.set_xticks(range(len(values)))
    ax.grid(axis="y", alpha=0.2)

    fig.tight_layout()

    chart_area.pyplot(fig)
    plt.close(fig)


draw_chart(original)

st.write("**Original Array:**", original)

if st.button("▶️ START SORTING", type="primary"):

    if not original:
        st.error("Please enter some numbers.")

    else:
        events = sorting_steps(original, algorithm)

        progress = st.progress(0)

        status_area.info("Sorting in progress...")

        total = len(events)

        for step, event in enumerate(events):

            values, x, y, comp, swap = event

            draw_chart(values, x, y)

            with stats_area.container():
                m1, m2, m3 = st.columns(3)

                m1.metric("Comparisons", comp)
                m2.metric("Swaps / Moves", swap)
                m3.metric("Steps", step + 1)

            progress.progress((step + 1) / total)

            time.sleep(speed)

        draw_chart(values)

        status_area.success("🎉 Sorting Completed Successfully!")

        st.success(
            "Final Sorted Array: "
            + str(values)
        )

        st.balloons()

st.divider()

st.markdown("### 🧠 About Selected Algorithm")

descriptions = {
    "Bubble Sort":
        "Compares adjacent elements and swaps them if they are in the wrong order.",

    "Selection Sort":
        "Finds the smallest element and places it at the correct position.",

    "Insertion Sort":
        "Takes one element at a time and inserts it into its correct position.",

    "Merge Sort":
        "Divides the array into smaller parts, sorts them and merges them.",

    "Quick Sort":
        "Selects a pivot and partitions the array into smaller and larger elements."
}

st.info(descriptions[algorithm])

st.markdown("---")
st.caption(
    "DAA Mini Project | Sorting Algorithm Visualizer | "
    "Developed using Python and Streamlit"
)
