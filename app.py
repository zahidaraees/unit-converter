# Import of Dependencies
import streamlit as st
from pint import UnitRegistry
from collections import deque

# Initialization of Unit Registry
ureg = UnitRegistry()

# To store Conversion History using session state
if 'history' not in st.session_state:
    st.session_state.history = deque(maxlen=10)
history = st.session_state.history  # Use session state for history

# Defining Unit Categories
unit_categories = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
    "Mass": ["kilogram", "gram", "milligram", "pound", "ounce"],
    "Volume": ["liter", "milliliter", "gallon", "quart", "pint", "cup", "fluid_ounce"],
    "Time": ["second", "minute", "hour", "day"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour"],
    "Area": ["square_meter", "square_kilometer", "square_mile", "acre", "hectare"],
    "Data Storage": ["byte", "kilobyte", "megabyte", "gigabyte", "terabyte"]
}

# Title and Description (Centralized with Icons)
st.markdown("""
    <h1 style='text-align: center;'>🔄 Unit Converter</h1>
    <p style='text-align: center; font-size: 18px;'>🔢 Convert units across multiple categories with ease!</p>
    <p style='text-align: center; font-size: 16px;'>👩‍💻 Developed by Zahida Raees</p>
""", unsafe_allow_html=True)

# Category Selection with Icon
category = st.selectbox("📂 Select Category:", list(unit_categories.keys()))

# Dynamic Units, based on Category
units = unit_categories[category]
source_unit = st.selectbox("🔄 From Unit:", units)
target_unit = st.selectbox("➡️ To Unit:", units)

# Input Value with Icon
value = st.number_input("🔢 Enter the value to convert:", min_value=0.0, value=1.0)

# Perform Conversion, based on Category.
if st.button("🚀 Convert"):
    try:
        # Handle Temperature Conversions Separately
        if category == "Temperature":
            if source_unit == "celsius" and target_unit == "fahrenheit":
                output_value = (value * 9/5) + 32
            elif source_unit == "fahrenheit" and target_unit == "celsius":
                output_value = (value - 32) * 5/9
            elif source_unit == "celsius" and target_unit == "kelvin":
                output_value = value + 273.15
            elif source_unit == "kelvin" and target_unit == "celsius":
                output_value = value - 273.15
            elif source_unit == "fahrenheit" and target_unit == "kelvin":
                output_value = ((value - 32) * 5/9) + 273.15
            elif source_unit == "kelvin" and target_unit == "fahrenheit":
                output_value = ((value - 273.15) * 9/5) + 32
            else:
                output_value = value  # Same Unit Conversion
        else:
            input_value = value * ureg(source_unit)
            output_value = input_value.to(target_unit).magnitude

        # Display Result with Icon
        result = f"🎉 {value} {source_unit} = {output_value:.4f} {target_unit}"
        st.success(result)

        # Add to History using session state
        history.appendleft(result)

    except Exception as e:
        st.error("❌ Conversion not possible. Please check the units.")

# Display Conversion History with Icon
st.subheader("📜 Conversion History")
if history:
    for i, record in enumerate(history, 1):
        st.write(f"{i}. {record}")
else:
    st.info("📭 No conversions yet.")

# Sidebar Documentation
st.sidebar.title("📘 Documentation")

st.sidebar.subheader("Overview")
st.sidebar.markdown("""
This Unit Converter is built using **Streamlit** and **Pint** for accurate unit conversions.
It supports multiple categories such as:
- Length
- Mass
- Volume
- Time
- Temperature
- Speed
- Area
- Data Storage
""")

st.sidebar.subheader("How It Works")
st.sidebar.markdown("""
1. **Select Category:** Choose the category of units you want to convert.
2. **Choose Units:** Select the source and target units.
3. **Enter Value:** Input the value to be converted.
4. **Convert:** Click the Convert button to see the result.
5. **History:** The last 10 conversions are displayed below.
""")

st.sidebar.subheader("Features and Improvements")
st.sidebar.markdown("""
- **Dynamic Unit Filtering** based on selected category.
- **Conversion History** is displayed in real-time.
- **Error Handling** for unsupported conversions.
- **Responsive Design** for mobile and desktop.
""")

if st.button("🧹 Clear History"):
    history.clear()  # Clear the deque object directly
    st.session_state.history = history  # Update the session state
    st.rerun()  # Force immediate rerun (new method)

    
