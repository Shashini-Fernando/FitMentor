import streamlit as st
import pandas as pd
from generator import generate_fitness_plan

# Set page configuration for better layout
st.set_page_config(page_title="FitMentor", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for attractive interface
st.markdown("""
    <style>
    /* Global styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f4f8;
    }
    .stApp {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e3a8a;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        color: #ffffff;
    }
    .sidebar .stButton>button {
        background-color: #f97316;
        color: #ffffff;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        width: 100%;
        transition: background-color 0.3s;
    }
    .sidebar .stButton>button:hover {
        background-color: #ea580c;
    }
    /* Main content styling */
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #f97316;
        color: #ffffff;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #ea580c;
    }
    .stSelectbox, .stTextInput {
        background-color: #f0f4f8;
        border-radius: 8px;
        padding: 10px;
    }
    .stMarkdown p {
        color: #334155;
        line-height: 1.6;
    }
    .stSuccess, .stInfo {
        border-radius: 8px;
        padding: 15px;
    }
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and questions
st.sidebar.title("FitMentor Navigation")
st.sidebar.markdown("Welcome to your fitness journey! Select an option or question below.", unsafe_allow_html=True)

# User input section
with st.sidebar.form("user_input_form"):
    st.subheader("Your Profile")
    goal = st.text_input("Fitness Goal (e.g., weight loss, muscle gain)")
    level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    diet = st.text_input("Dietary Preferences (e.g., low-carb, vegetarian)")
    submit_profile = st.form_submit_button("Save Profile")

# Predefined questions and answers
questions = {
    "What exercises should I do?": lambda goal, level, diet: f"For your {goal} goal as a {level}, try {', '.join([w['name'] for w in generate_fitness_plan(goal, level, diet)[:3]])} exercises. Adjust intensity based on your comfort.",
    "How many calories should I eat?": lambda goal, level, diet: f"Based on your {goal} goal, aim for {1500 if goal.lower() == 'weight loss' else 2500} calories daily, adjusted for your {level} activity level and {diet} diet.",
    "How often should I workout?": lambda goal, level, diet: f"As a {level} aiming for {goal}, workout 7 days a week with varied intensity to support recovery.",
    "What should I eat before a workout?": lambda goal, level, diet: f"Before a workout, eat a {diet} snack like {('Greek Yogurt' if diet.lower() == 'vegetarian' else 'Eggs') if level == 'Beginner' else 'Protein Shake'} 30 minutes prior for energy.",
    "How should I recover after a workout?": lambda goal, level, diet: f"After a workout, focus on recovery by stretching for 5-10 minutes and consuming a {diet} meal like {('Quinoa Stir-Fry' if diet.lower() == 'vegetarian' else 'Grilled Chicken Salad')} within 2 hours to replenish energy.",
    "When should I eat my meals for best results?": lambda goal, level, diet: f"For {goal}, eat small meals every 3-4 hours. Start with breakfast within 1 hour of waking, and have a {diet} post-workout meal within 2 hours of exercise to optimize energy and recovery.",
    "How much water should I drink daily?": lambda goal, level, diet: f"As a {level} aiming for {goal}, drink at least {2 if level == 'Beginner' else 3} liters of water daily. Increase to {3 if level == 'Beginner' else 4} liters on workout days to stay hydrated.",
    "How can I track my progress effectively?": lambda goal, level, diet: f"To track your {goal} progress, measure your {('weight weekly' if goal.lower() == 'weight loss' else 'strength gains monthly')} and log your workouts. Adjust your {diet} meals if you’re not seeing results after 4 weeks.",
    "Should I vary my workouts?": lambda goal, level, diet: f"Yes, varying your workouts prevents plateaus. As a {level} aiming for {goal}, include {('cardio and strength' if goal.lower() == 'weight loss' else 'strength and powerlifting')} exercises weekly to keep progressing.",
    "How much sleep do I need for fitness?": lambda goal, level, diet: f"For optimal fitness as a {level}, aim for {7 if level == 'Beginner' else 8} hours of sleep per night. Sleep helps recovery, especially with your {goal} goal.",
    "Do I need supplements for my goals?": lambda goal, level, diet: f"Supplements depend on your {diet} diet and {goal}. {('A protein shake can help with muscle gain' if goal.lower() == 'muscle gain' else 'Focus on whole foods for weight loss, but a multivitamin can help')} as a {level}—consult a doctor first.",
    "How can I stay motivated to workout?": lambda goal, level, diet: f"To stay motivated for {goal} as a {level}, set small weekly goals (e.g., complete 7 workouts), track progress, and reward yourself with a {diet} treat like {('a smoothie' if diet.lower() == 'vegetarian' else 'a protein bar')}."
}

# Main content
st.title("FitMentor 💪")
st.markdown("Your Personal Fitness Coach - Let’s Build Your Plan!", unsafe_allow_html=True)

# Display saved profile if submitted
if 'profile_submitted' in st.session_state and st.session_state.profile_submitted:
    st.success("Profile saved! Here’s your personalized plan and answers.")
    goal = st.session_state.get('goal', goal)
    level = st.session_state.get('level', level)
    diet = st.session_state.get('diet', diet)

    # Generate fitness plan
    fitness_options = generate_fitness_plan(goal, level, diet)
    df = pd.DataFrame(fitness_options)

    # Define the order of days
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Default workout for days with no plan
    default_workout = {
        "workout_name": "Light Cardio & Stretching",
        "workout_type": "Cardio",
        "duration_min": 20,
        "calories_burned": 150
    }

    # Ensure every day has a workout
    workout_plan = []
    for day in days_of_week:
        day_workouts = df[df['day'] == day]
        if not day_workouts.empty and any(day_workouts["workout_name"].notna()):
            for _, row in day_workouts.iterrows():
                if row["workout_name"]:
                    workout_plan.append({
                        "day": day,
                        "workout_name": row["workout_name"],
                        "workout_type": row["workout_type"],
                        "duration_min": row["duration_min"],
                        "calories_burned": row["calories_burned"]
                    })
        else:
            workout_plan.append({
                "day": day,
                "workout_name": default_workout["workout_name"],
                "workout_type": default_workout["workout_type"],
                "duration_min": default_workout["duration_min"],
                "calories_burned": default_workout["calories_burned"]
            })

    # Workout plan display
    st.subheader("Weekly Workout Plan")
    for workout in workout_plan:
        st.markdown(
            f"- **{workout['day']}**: {workout['workout_type']} - {workout['workout_name']} "
            f"({workout['duration_min']} min, {workout['calories_burned']} cal burned)",
            unsafe_allow_html=True
        )

    # Meal plan
    st.subheader("Weekly Meal Plan")
    for day in days_of_week:
        day_meals = df[df['day'] == day]
        if not day_meals.empty:
            for _, row in day_meals.iterrows():
                if row["meal_name"]:
                    st.markdown(
                        f"- **{day}**: {row['meal_type']} - {row['meal_name']} "
                        f"({row['meal_calories']} cal, {row['meal_protein']}g protein)",
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                f"- **{day}**: No specific meal planned (Follow your {diet} diet guidelines)",
                unsafe_allow_html=True
            )

    # Question and answer section
    st.subheader("Ask a Question")
    selected_question = st.selectbox("Choose a question:", list(questions.keys()))
    if st.button("Get Answer"):
        answer = questions[selected_question](goal, level, diet)
        st.markdown(f"**Answer**: {answer}", unsafe_allow_html=True)

    # Display plan details
    st.subheader("Plan Details")
    st.dataframe(df)

    # Reasoning
    st.subheader("Reasoning")
    st.markdown(
        f"This plan is tailored for a {level} aiming for {goal}. Workouts are scheduled every day "
        f"to match your fitness level, with light activities on days without specific plans. "
        f"Meals align with your {diet} preference for balanced nutrition.",
        unsafe_allow_html=True
    )

# Save profile to session state
if submit_profile:
    st.session_state.profile_submitted = True
    st.session_state.goal = goal
    st.session_state.level = level
    st.session_state.diet = diet
    st.rerun()

# Initial instructions if no profile
if 'profile_submitted' not in st.session_state:
    st.info("Please fill out your profile in the sidebar to get started!")