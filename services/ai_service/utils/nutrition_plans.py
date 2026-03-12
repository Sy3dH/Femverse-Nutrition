# Base Plan Templates - Selected by User
PLAN_TEMPLATES = {
    "standard_balanced": """
    Plan: Standard Balanced Plan
    Goal: Maintain weight with balanced nutrition
    Calories: Maintenance level (BMR × activity factor)
    Macros: 30% protein, 40% carbs, 30% fats
    Focus: General health, variety of whole foods, balanced meals
    Principles: Include all food groups, colorful vegetables, whole grains, lean proteins, healthy fats
    """,

    "weight_loss": """
    Plan: Weight Loss Plan
    Goal: Sustainable fat loss while preserving muscle
    Calories: 20% deficit below maintenance
    Macros: 35% protein, 35% carbs, 30% fats
    Focus: High protein for satiety and muscle preservation, controlled portions, low-calorie dense foods
    Principles: Lean proteins at every meal, high-fiber vegetables, moderate complex carbs, avoid liquid calories
    Avoid: Processed foods, sugary snacks, high-calorie sauces
    """,

    "weight_gain": """
    Plan: Weight Gain / High-Calorie Plan
    Goal: Healthy weight gain or support high activity levels
    Calories: 15-20% surplus above maintenance
    Macros: 25% protein, 45% carbs, 30% fats
    Focus: Nutrient-dense foods, calorie-rich whole foods, frequent meals
    Principles: Nuts, nut butters, avocados, whole grains, dried fruits, smoothies with calories
    Strategy: 5-6 meals per day, add healthy fats to meals, calorie-dense snacks
    """,

    "pcos_friendly": """
    Plan: PCOS-Friendly Plan
    Goal: Manage insulin levels, reduce inflammation, hormone balance
    Calories: Based on weight goal (maintenance or deficit)
    Macros: 30% protein, 35% carbs (low-GI only), 35% fats (healthy fats)
    Focus: Low refined carbs/sugar, high fiber (25g+ daily), anti-inflammatory foods
    Include: Leafy greens, fatty fish (omega-3), nuts, seeds, whole grains (quinoa, oats), berries, turmeric, cinnamon
    Avoid: White bread, white rice, sugary foods, processed carbs, trans fats
    Special: Chromium-rich foods, spearmint tea, inositol considerations
    """,

    "pregnancy_t1": """
    Plan: Pregnancy Plan - First Trimester (Weeks 1-13)
    Goal: Support early fetal development, manage nausea
    Calories: Maintenance (no extra calories needed)
    Macros: 25% protein, 45% carbs, 30% fats
    Focus: Folate (600 mcg), B6, small frequent meals for nausea
    Critical Nutrients: Folate/Folic acid, Iron (27mg), Calcium (1000mg), Protein (71g+), DHA (200-300mg)
    Include: Leafy greens, fortified cereals, legumes, citrus, ginger, bland crackers
    Avoid: Raw fish, deli meats, unpasteurized dairy, high-mercury fish, alcohol, excess caffeine
    Nausea tips: Ginger tea, small meals, protein-rich snacks, avoid strong smells
    """,

    "pregnancy_t2": """
    Plan: Pregnancy Plan - Second Trimester (Weeks 14-27)
    Goal: Support rapid fetal growth, maintain maternal health
    Calories: Maintenance + 300 kcal
    Macros: 25% protein, 45% carbs, 30% fats
    Focus: Iron, calcium, protein, DHA, vitamin D
    Critical Nutrients: Iron (27mg), Calcium (1000mg), Protein (71g+), DHA (200-300mg), Vitamin D (600 IU)
    Include: Lean meats, fortified dairy, fatty fish (salmon), dark leafy greens, eggs, legumes
    Strategy: Iron + Vitamin C for absorption, calcium sources throughout day
    """,

    "pregnancy_t3": """
    Plan: Pregnancy Plan - Third Trimester (Weeks 28-40)
    Goal: Support final growth phase, prepare for delivery, prevent constipation
    Calories: Maintenance + 450 kcal
    Macros: 30% protein, 40% carbs, 30% fats
    Focus: Iron, calcium, protein (80g+), fiber, DHA
    Critical Nutrients: Iron, Calcium, Protein (80-100g), DHA, Vitamin K, Fiber (28g+)
    Include: Red meat (iron), dairy, fatty fish, prunes, high-fiber foods, plenty of water
    Strategy: Small frequent meals (digestion slows), prevent constipation with fiber + water
    """,

    "postpartum": """
    Plan: Postpartum / Lactation Plan
    Goal: Support recovery, milk production (if breastfeeding), replenish nutrients
    Calories: Maintenance + 500 kcal (if breastfeeding), Maintenance + 200 kcal (if not)
    Macros: 25% protein, 40% carbs, 35% fats
    Focus: High protein for healing, hydration (3L+ water), nutrient replenishment
    Critical Nutrients: Protein (71g+), Calcium (1000mg), Iron, Vitamin D, Omega-3, B vitamins, Choline
    Include: Lean proteins, oats (lactation), leafy greens, nuts, seeds, fatty fish, hydrating foods
    Lactation support: Oats, flaxseed, fennel, fenugreek, adequate hydration
    Recovery: Iron-rich foods (blood loss recovery), protein for tissue repair
    """,

    "preconception": """
    Plan: Pre-Conception Plan
    Goal: Optimize fertility, prepare body for pregnancy
    Calories: Maintenance (achieve healthy BMI if needed)
    Macros: 30% protein, 40% carbs, 30% fats
    Focus: Folate, iron, antioxidants, healthy fats, blood sugar balance
    Critical Nutrients: Folate (400-800 mcg), Iron, Zinc, Vitamin D, CoQ10, Omega-3, Antioxidants
    Include: Leafy greens, berries, nuts, seeds, fatty fish, whole grains, legumes, colorful vegetables
    For men: Zinc, selenium, antioxidants (for sperm health)
    Avoid: Trans fats, excess alcohol, high-mercury fish, processed foods
    """,

    "gluten_free": """
    Plan Modifier: Gluten-Free (applies to any base plan)
    Restriction: No gluten (wheat, barley, rye, contaminated oats)
    Replacements: Rice, quinoa, certified GF oats, corn, buckwheat, millet, almond flour, coconut flour
    Focus: Naturally gluten-free whole foods (vegetables, fruits, proteins, dairy)
    Watch for: Hidden gluten in sauces, seasonings, processed foods
    Include: GF whole grains, naturally GF proteins, plenty of vegetables and fruits
    """,

    "vegetarian": """
    Plan Modifier: Vegetarian (applies to any base plan)
    Restriction: No meat, poultry, fish (may include eggs and dairy if lacto-ovo)
    Protein Sources: Legumes (beans, lentils), tofu, tempeh, eggs, dairy, Greek yogurt, cottage cheese, quinoa
    Critical Nutrients: B12 (fortified foods or supplement), Iron (with Vitamin C), Zinc, Omega-3 (flax, chia, walnuts)
    Include: Variety of plant proteins, iron-rich plants + citrus, nuts, seeds
    Strategy: Combine incomplete proteins (rice + beans), fortified plant milks
    """,

    "vegan": """
    Plan Modifier: Vegan (applies to any base plan)
    Restriction: No animal products (meat, dairy, eggs, honey)
    Protein Sources: Legumes, tofu, tempeh, seitan, edamame, quinoa, nuts, seeds, plant-based protein powders
    Critical Nutrients: B12 (supplement required), Iron + Vitamin C, Calcium (fortified), Vitamin D, Zinc, Omega-3 (algae-based), Iodine
    Include: Fortified plant milks, nutritional yeast (B12), varied plant proteins, dark leafy greens
    Strategy: Supplement B12, combine proteins, use fortified foods, consider algae omega-3
    """,

    "diabetic_low_gi": """
    Plan: Diabetic-Friendly / Low-GI Plan
    Goal: Stable blood sugar, prevent spikes, manage diabetes/prediabetes
    Calories: Based on weight goal
    Macros: 25% protein, 40% carbs (low-GI only), 35% fats
    Focus: Low glycemic index foods, high fiber (30g+), consistent carb portions per meal
    Include: Non-starchy vegetables, whole grains (oats, quinoa, barley), legumes, nuts, lean proteins
    Avoid: White bread, white rice, sugary foods, fruit juices, high-GI carbs
    Strategy: Pair carbs with protein/fat, consistent meal timing, portion control
    Monitoring: Track carb intake per meal (45-60g typical)
    """,

    "wedding_prep": """
    Plan: Wedding Prep Plan (Time-Sensitive Weight Loss)
    Goal: Sustainable weight loss with skin health focus for special event
    Calories: 15-20% deficit (more aggressive than standard weight loss)
    Macros: 35% protein, 35% carbs, 30% fats
    Focus: Fat loss, muscle preservation, glowing skin, energy levels
    Skin Health: Vitamin C (collagen), Vitamin E, Omega-3 (anti-inflammatory), hydration (3L+ water)
    Include: Berries, citrus, fatty fish, nuts, leafy greens, lean proteins, colorful vegetables
    Timeline Strategy: 
    - 3+ months out: Moderate deficit, establish habits
    - 1-3 months: Maintain deficit, focus on consistency
    - 2 weeks before: Increase water, reduce bloating foods (salt, processed)
    Avoid: Crash dieting, extreme restrictions, alcohol (bloating)
    """,

    "exam_brain_boost": """
    Plan: Exam Energy / Brain Boost Plan
    Goal: Optimize cognitive function, sustained energy, focus, memory
    Calories: Maintenance
    Macros: 25% protein, 45% carbs (complex), 30% fats
    Focus: Omega-3 (DHA for brain), B vitamins, antioxidants, sustained energy (no crashes)
    Brain Foods: Fatty fish (salmon, sardines), walnuts, blueberries, dark chocolate, eggs, avocado
    Include: Whole grains, leafy greens, berries, nuts, seeds, green tea, dark chocolate (70%+)
    Energy Strategy: Complex carbs for steady glucose, avoid sugar crashes
    Study Snacks: Nuts + berries, hummus + veggies, Greek yogurt + walnuts, dark chocolate
    Hydration: Critical for focus (dehydration impairs cognition)
    Avoid: Energy drinks (crash), high sugar (blood sugar swings), heavy meals (drowsiness)
    """,

    "high_protein_athletic": """
    Plan: High-Protein / Athletic Performance Plan
    Goal: Muscle building, recovery, athletic performance
    Calories: Based on activity level (maintenance to surplus)
    Macros: 40% protein, 35% carbs, 25% fats
    Protein Target: 1.6-2.2g per kg body weight
    Focus: Protein timing (post-workout), recovery, electrolytes, energy for training
    Include: Lean meats, fish, eggs, Greek yogurt, protein powder, quinoa, sweet potatoes
    Timing: Protein within 30-60 min post-workout, carbs around training
    Pre-Workout: Carbs + moderate protein (2-3 hours before)
    Post-Workout: Protein + carbs (3:1 or 4:1 ratio)
    Hydration: Electrolytes during/after intense exercise
    Recovery: Anti-inflammatory foods (berries, fatty fish, turmeric)
    """
}