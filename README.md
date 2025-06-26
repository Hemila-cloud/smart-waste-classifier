
#  Smart Waste Management System

Smart Waste Management System is an AI-powered, interactive dashboard designed to modernize municipal waste collection by combining real-time bin monitoring, automated waste classification, and route optimization into a unified, user-friendly platform.

## Key Features

- **Real-Time Bin Monitoring:**  
  Track garbage bin locations and fill levels using a dynamic map.  
  Color-coded indicators highlight bins that need immediate attention.

- **Waste Classification Using AI:**  
  Upload an image of waste (plastic, metal, e-waste, etc.).  
  The system uses a pretrained deep learning model to predict the category and confidence level.

- **Optimized Truck Routing:**  
  Automatically generate efficient collection routes based on bin fill percentage.  
  Prioritizes bins that are more than 80% full.

## How It Works

1. **Frontend Dashboard (Streamlit):**  
   Built with tabbed navigation for bin monitoring, waste classification, and route planning.  
   Visualizations built using Plotly, Folium, and interactive file upload components.

2. **AI Waste Classifier:**  
   Employs MobileNetV2 pretrained on ImageNet for object recognition.  
   Can be upgraded to a domain-specific model trained on waste datasets (e.g., TrashNet).

3. **Bin Simulation & Routing:**  
   Bin data is simulated for testing (location, fill level).  
   Route optimization is based on simple heuristics prioritizing overflow bins.


##  Run the App
streamlit run app.py

## 🌱 Future Enhancements

- Train a custom waste classifier on domain-specific datasets  
- Integrate GPS from smart bins for live tracking  
- Add user authentication for role-based access (e.g., admin, driver)  






