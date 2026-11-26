
from flask import Flask, jsonify, request, session, render_template
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "brain-battle-development-key"
)

QUESTIONS_PER_ROUND = 5

# NCERT Class 11 starter question bank
BANK = {
    "Physics": [
        {
            "chapter": "Units and Measurements",
            "q": "What is the SI unit of length?",
            "o": ["Metre", "Kilogram", "Second", "Newton"],
            "a": 0
        },
        {
            "chapter": "Units and Measurements",
            "q": "How many significant figures are there in 0.00520?",
            "o": ["2", "3", "4", "5"],
            "a": 1
        },
        {
            "chapter": "Motion in a Straight Line",
            "q": "The slope of a position-time graph represents:",
            "o": ["Acceleration", "Velocity", "Force", "Momentum"],
            "a": 1
        },
        {
            "chapter": "Motion in a Straight Line",
            "q": "What is the SI unit of acceleration?",
            "o": ["m/s", "m/s²", "km/h", "Newton"],
            "a": 1
        },
        {
            "chapter": "Motion in a Plane",
            "q": "Which of these is a vector quantity?",
            "o": ["Mass", "Speed", "Velocity", "Time"],
            "a": 2
        },
        {
            "chapter": "Laws of Motion",
            "q": "Newton's first law is also known as:",
            "o": ["Law of inertia", "Law of force",
                  "Law of action", "Law of energy"],
            "a": 0
        },
        {
            "chapter": "Laws of Motion",
            "q": "The SI unit of force is:",
            "o": ["Joule", "Newton", "Watt", "Pascal"],
            "a": 1
        },
        {
            "chapter": "Work, Energy and Power",
            "q": "What is the SI unit of work?",
            "o": ["Watt", "Newton", "Joule", "Pascal"],
            "a": 2
        },
        {
            "chapter": "Work, Energy and Power",
            "q": "Kinetic energy depends on:",
            "o": ["Mass and speed", "Only mass",
                  "Only height", "Only force"],
            "a": 0
        },
        {
            "chapter": "Gravitation",
            "q": "What is the approximate value of g near Earth's surface?",
            "o": ["3.8 m/s²", "9.8 m/s²",
                  "15 m/s²", "20 m/s²"],
            "a": 1
        },
        {
            "chapter": "Thermodynamics",
            "q": "The SI unit of temperature is:",
            "o": ["Celsius", "Fahrenheit", "Kelvin", "Joule"],
            "a": 2
        },
        {
            "chapter": "Oscillations",
            "q": "The SI unit of frequency is:",
            "o": ["Hertz", "Metre", "Second", "Newton"],
            "a": 0
        }
    ],

    "Chemistry": [
        {
            "chapter": "Some Basic Concepts",
            "q": "What is the SI unit of amount of substance?",
            "o": ["Gram", "Mole", "Litre", "Kilogram"],
            "a": 1
        },
        {
            "chapter": "Some Basic Concepts",
            "q": "Avogadro constant is approximately:",
            "o": ["6.022 × 10²³", "3 × 10⁸",
                  "9.8", "1.6 × 10⁻¹⁹"],
            "a": 0
        },
        {
            "chapter": "Structure of Atom",
            "q": "Who discovered the electron?",
            "o": ["Rutherford", "Bohr",
                  "J.J. Thomson", "Dalton"],
            "a": 2
        },
        {
            "chapter": "Structure of Atom",
            "q": "Which particle has no electric charge?",
            "o": ["Proton", "Electron", "Neutron", "Positron"],
            "a": 2
        },
        {
            "chapter": "Classification of Elements",
            "q": "The modern periodic law is based on:",
            "o": ["Atomic mass", "Atomic number",
                  "Neutron number", "Atomic volume"],
            "a": 1
        },
        {
            "chapter": "Chemical Bonding",
            "q": "Which bond involves sharing of electrons?",
            "o": ["Ionic", "Covalent", "Metallic only", "Hydrogen"],
            "a": 1
        },
        {
            "chapter": "Chemical Bonding",
            "q": "What is the shape of a methane molecule?",
            "o": ["Linear", "Bent", "Tetrahedral", "Trigonal planar"],
            "a": 2
        },
        {
            "chapter": "Thermodynamics",
            "q": "An exothermic reaction releases:",
            "o": ["Heat", "Light only", "No energy", "Matter"],
            "a": 0
        },
        {
            "chapter": "Equilibrium",
            "q": "What does pH 7 indicate at 25°C?",
            "o": ["Acidic", "Basic", "Neutral", "Strong acid"],
            "a": 2
        },
        {
            "chapter": "Redox Reactions",
            "q": "Oxidation involves:",
            "o": ["Gain of electrons", "Loss of electrons",
                  "Gain of protons", "Loss of neutrons"],
            "a": 1
        },
        {
            "chapter": "Organic Chemistry",
            "q": "The tetravalency of carbon means it forms:",
            "o": ["One bond", "Two bonds",
                  "Three bonds", "Four bonds"],
            "a": 3
        },
        {
            "chapter": "Hydrocarbons",
            "q": "What is the general formula of alkanes?",
            "o": ["CnH2n", "CnH2n+2", "CnH2n-2", "CnHn"],
            "a": 1
        }
    ],

    "Mathematics": [
        {
            "chapter": "Sets",
            "q": "A set with no elements is called:",
            "o": ["Universal set", "Empty set",
                  "Equal set", "Finite set"],
            "a": 1
        },
        {
            "chapter": "Sets",
            "q": "How many subsets does a set with 3 elements have?",
            "o": ["3", "6", "8", "9"],
            "a": 2
        },
        {
            "chapter": "Relations and Functions",
            "q": "A function assigns each input:",
            "o": ["Exactly one output", "Two outputs",
                  "No output", "Any number of outputs"],
            "a": 0
        },
        {
            "chapter": "Trigonometric Functions",
            "q": "What is sin 90°?",
            "o": ["0", "1", "-1", "1/2"],
            "a": 1
        },
        {
            "chapter": "Trigonometric Functions",
            "q": "What is cos 0°?",
            "o": ["0", "1", "-1", "1/2"],
            "a": 1
        },
        {
            "chapter": "Complex Numbers",
            "q": "What is the value of i²?",
            "o": ["1", "-1", "i", "0"],
            "a": 1
        },
        {
            "chapter": "Linear Inequalities",
            "q": "If x > 2, which value satisfies the inequality?",
            "o": ["1", "2", "3", "0"],
            "a": 2
        },
        {
            "chapter": "Permutations and Combinations",
            "q": "What is 5 factorial?",
            "o": ["25", "60", "100", "120"],
            "a": 3
        },
        {
            "chapter": "Binomial Theorem",
            "q": "What is the coefficient of x in (1+x)²?",
            "o": ["1", "2", "3", "4"],
            "a": 1
        },
        {
            "chapter": "Sequences and Series",
            "q": "What is the common difference of 2, 5, 8, 11?",
            "o": ["2", "3", "4", "5"],
            "a": 1
        },
        {
            "chapter": "Straight Lines",
            "q": "What is the slope of a horizontal line?",
            "o": ["0", "1", "Undefined", "-1"],
            "a": 0
        },
        {
            "chapter": "Limits and Derivatives",
            "q": "The derivative of x² with respect to x is:",
            "o": ["x", "2x", "x²", "2"],
            "a": 1
        }
    ],

    "Computer Science": [
        {
            "chapter": "Computer Systems",
            "q": "Which component is called the brain of a computer?",
            "o": ["Monitor", "CPU", "Keyboard", "Mouse"],
            "a": 1
        },
        {
            "chapter": "Computer Systems",
            "q": "Which memory is volatile?",
            "o": ["ROM", "Hard disk", "RAM", "DVD"],
            "a": 2
        },
        {
            "chapter": "Python Basics",
            "q": "Which keyword defines a function in Python?",
            "o": ["function", "define", "def", "fun"],
            "a": 2
        },
        {
            "chapter": "Python Basics",
            "q": "Which symbol is used for Python comments?",
            "o": ["//", "#", "/*", "$"],
            "a": 1
        },
        {
            "chapter": "Python Data Types",
            "q": "Which data type stores True or False?",
            "o": ["int", "str", "bool", "float"],
            "a": 2
        },
        {
            "chapter": "Python Operators",
            "q": "What is the output of 10 // 3?",
            "o": ["3.33", "3", "1", "4"],
            "a": 1
        },
        {
            "chapter": "Python Operators",
            "q": "Which operator is used for exponentiation?",
            "o": ["^", "**", "//", "%"],
            "a": 1
        },
        {
            "chapter": "Python Programming",
            "q": "Which function displays output in Python?",
            "o": ["input()", "print()", "show()", "write()"],
            "a": 1
        },
        {
            "chapter": "Python Programming",
            "q": "Which loop is commonly used to iterate over a sequence?",
            "o": ["for", "switch", "case", "repeat"],
            "a": 0
        },
        {
            "chapter": "Python Strings",
            "q": "Which data type stores text?",
            "o": ["int", "float", "str", "bool"],
            "a": 2
        },
        {
            "chapter": "Python Lists",
            "q": "Python list indexing normally starts from:",
            "o": ["0", "1", "-1", "2"],
            "a": 0
        },
        {
            "chapter": "Python Functions",
            "q": "Which statement sends a value back from a function?",
            "o": ["print", "break", "return", "continue"],
            "a": 2
        }
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/questions")
def get_questions():
    subject = request.args.get("subject")

    if subject not in BANK:
        return jsonify({"error": "Invalid subject"}), 400

    pool = BANK[subject]

    # Previous question IDs for this subject
    history = session.get("history", {})
    previous = history.get(subject, [])

    # Exclude questions used in earlier rounds
    available = [
        i for i in range(len(pool))
        if i not in previous
    ]

    # Reset cycle only when fewer than 5 fresh questions remain
    if len(available) < QUESTIONS_PER_ROUND:
        available = list(range(len(pool)))
        previous = []

    selected = random.sample(
        available, QUESTIONS_PER_ROUND
    )

    # Save history in browser session
    history[subject] = previous + selected
    session["history"] = history

    result = []

    for index in selected:
        original = pool[index]

        # Shuffle options and preserve correct answer
        options = list(enumerate(original["o"]))
        random.shuffle(options)

        correct_position = next(
            i for i, item in enumerate(options)
            if item[0] == original["a"]
        )

        result.append({
            "id": index,
            "chapter": original["chapter"],
            "q": original["q"],
            "o": [item[1] for item in options],
            "a": correct_position
        })

    return jsonify({
        "subject": subject,
        "total": len(pool),
        "questions": result
    })


@app.route("/api/reset", methods=["POST"])
def reset_history():
    session.pop("history", None)
    return jsonify({"message": "Question history reset"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
