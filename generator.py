import random

def generate_fitness_plan(goal, level, diet):
    """
    Generate mock workout and meal options for a given goal, level, and diet.
    Returns a list of dictionaries with workout and meal details.
    """
    # Mock data for workouts
    workouts = {
        "weight loss": [
            {"type": "Cardio", "name": "Running", "duration_min": 30, "calories_burned": 300, "level": "Beginner"},
            {"type": "Cardio", "name": "Cycling", "duration_min": 45, "calories_burned": 400, "level": "Intermediate"},
            {"type": "HIIT", "name": "High-Intensity Interval", "duration_min": 20, "calories_burned": 250, "level": "Advanced"}
        ],
        "muscle gain": [
            {"type": "Strength", "name": "Weight Lifting", "duration_min": 60, "calories_burned": 350, "level": "Beginner"},
            {"type": "Strength", "name": "Resistance Training", "duration_min": 75, "calories_burned": 450, "level": "Intermediate"},
            {"type": "Powerlifting", "name": "Heavy Lifts", "duration_min": 90, "calories_burned": 500, "level": "Advanced"}
        ]
    }
    
    # Mock data for meals
    meals = {
        "low-carb": [
            {"type": "Breakfast", "name": "Egg Muffins", "calories": 180, "protein": 15},
            {"type": "Lunch", "name": "Grilled Chicken Salad", "calories": 300, "protein": 25},
            {"type": "Dinner", "name": "Salmon with Asparagus", "calories": 400, "protein": 30}
        ],
        "vegetarian": [
            {"type": "Breakfast", "name": "Greek Yogurt with Nuts", "calories": 250, "protein": 12},
            {"type": "Lunch", "name": "Lentil Curry", "calories": 350, "protein": 18},
            {"type": "Dinner", "name": "Quinoa Stir-Fry", "calories": 450, "protein": 20}
        ]
    }
    
    # Select workouts based on goal and level
    goal = goal.lower() if goal else "weight loss"
    selected_workouts = [w for w in workouts.get(goal, workouts["weight loss"]) if w["level"] == level]
    
    # Select meals based on diet
    diet = diet.lower() if diet else "low-carb"
    selected_meals = meals.get(diet, meals["low-carb"])  # Default to low-carb if diet not found
    
    # Generate plan for 5 days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    options = [
        {
            "day": days[i],
            "workout_type": w["type"],
            "workout_name": w["name"],
            "duration_min": w["duration_min"],
            "calories_burned": w["calories_burned"],
            "meal_type": m["type"],
            "meal_name": m["name"],
            "meal_calories": m["calories"],
            "meal_protein": m["protein"]
        }
        for i, (w, m) in enumerate(zip(random.sample(selected_workouts, min(5, len(selected_workouts))), 
                                       random.sample(selected_meals, min(3, len(selected_meals))) * (5 // 3 + 1)))
        if i < 5  # Limit to 5 days
    ]
    
    return options