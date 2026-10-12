import re
import difflib

QUESTIONS = [
    (
        "Home",
        "You indicated in the survey that you live in an apartment. "
        "Tell me about your home. What does it look like? "
        "What types of rooms does it have? Please describe it in detail.",
        """I live in a 3-bedroom apartment. When you walk into the front door, You can see an entrance area. Where you can take off your shoes.
On the left, There is my room. The living room is also to the left.
On the right is kitchen. Next to the kitchen, You can see a bathroom and a balcony.
My house is clean and modern"""
    ),
    (
        "Home",
        "Tell me about your bedroom. What does it look like and what "
        "do you keep in it? Use as many detail as possible to describe it.",
        """I think my room is clean and modern. I love my room because it's only for me.
I can have quiet moments all by myself without any distraction.
Another reason is that since my bedroom has large windows. I enjoy a breathtaking view and fresh air.
When you walk into a my room. You can see a bed. On the left there is a dressing table. A desk is also to the left.
On the right is bookshelf. I am satisfied with my room."""
    ),
    (
        "Home",
        "It is important for a family to spend time together. "
        "When do you spend time at home with your family? "
        "What does your family usually do at home?",
        """Well.. I am very busy during the week,
So I usually spend time with my family on weekends.
We usually prepare dinner together at home. I help mother cook and my brother does the dishes.
While having our meal, We often talk about current events. After dinner, Everyone relaxes.
My house is very cozy. So we enjoy spending time there.
My brother and I usually play video games together. My parents like to watch TV."""
    ),
    (
        "Home",
        "Have you made any changes to your house within the last few years? "
        "If so, what kinds of changes have you made to your home? "
        "Are you satisfied with the changes?",
        """I live in an apartment and I recently redecorated my living room.
I replaced the old wallpaper has a bright and modern design. It made the room brighter.
I also decided to get new furniture. I purchased a new couch and a matching chair.
Finally, I put up new curtains in the room.
I am very happy with my living room now"""
    ),
    (
        "Neighborhood and Neighbors",
        "You indicated in the survey that you live in an apartment. "
        "What is your neighborhood like? Where is it located? "
        "Please describe your neighborhood in detail.",
        """I live in the downtown of Seoul.
There are many restaurants and supermarkets in my neighborhood.
Also it has a good transportation system.
It's only a 5-minute walk to a subway station.
My neighborhood is very clean and nice.
I feel lucky to live in my neighborhood."""
    ),
    (
        "Neighborhood and Neighbors",
        "I would like to know about your neighbors. "
        "Who are they? What do they do? "
        "How often do you interact with them?",
        """I am close with one of my neighbors.
His name is sam. He lives right next to me.
He is a teacher who lives alone.
We have a lot in common.
I think we get together at least once a week.
We usually watch movies together.
We also go grocery shopping and go for a walk when we have time.
He is good neighbor who became my friend."""
    ),
    (
        "Neighborhood and Neighbors",
        "Can you tell me about an interesting or memorable experience "
        "you have had in your neighborhood? "
        "Tell me about the experience in detail and explain "
        "what made it so memorable.",
        """Yes, I had a special experience.
I was talking a walk in my neighborhood last year.
When I was walking, I ran into an old friend of mine.
My friend in my neighborhood! Can you believe it?
We went to same high school.
He told me he was shopping with his familly.
We met for a drink that night.
It was an amazing experience.
We became even better friends after that."""
    ),
    (
        "Neighborhood and Neighbors",
        "How was your neighborhood changed from when you were young? "
        "Describe in detail how it was in the past, and how it is now.",
        """Well.. My current neighborhood is very different from my old neighborhood.
When I was young, I lived in the countryside.
It was very quiet all the time and it had limited amenities.
It took more than 2 hours to a grocery store.
But now, I live in the downtown.
It's a busy city 24/7.
Everything is within walking distance so It's super convenient!
I love my current neighborhood."""
    ),
]


def normalize(text):
    # Ignore case, punctuation, and apostrophes.
    text = re.sub(r"['\u2019\u2018]", "", text.casefold())
    return re.findall(r"[^\W_]+", text)


def grade(answer, script):
    expected = normalize(script)
    actual = normalize(answer)

    if not actual:
        print("\nNo answer entered.")
        return False

    if actual == expected:
        print("\nCorrect!")
        return True

    print("\nSome parts are different.")
    matcher = difflib.SequenceMatcher(
        a=expected, b=actual, autojunk=False
    )

    for tag, a, b, c, d in matcher.get_opcodes():
        if tag == "equal":
            continue

        context = " ".join(expected[max(0, a - 4):a])
        print(
            "\nLocation:",
            f"After '{context}'" if context else "Start of answer"
        )

        if tag == "delete":
            print("Missing words:", " ".join(expected[a:b]))
        elif tag == "insert":
            print("Extra words:", " ".join(actual[c:d]))
        else:
            print("Your answer:", " ".join(actual[c:d]))
            print("Expected:   ", " ".join(expected[a:b]))

    return False


def main():
    print("OPIC Script Quiz")
    print("After writing your answer, type /end on a new line.")
    print("/answer: Show script | /next: Next question | /quit: Exit")

    index = 0

    while True:
        topic, question, script = QUESTIONS[index]

        print("\n" + "=" * 45)
        print(f"Topic: {topic}")
        print(f"Question {index + 1} / {len(QUESTIONS)}")
        print(question)
        print("=" * 45)

        lines = []

        while True:
            line = input()
            command = line.strip().lower()

            if command == "/quit":
                print("Quiz ended.")
                return

            if command == "/answer":
                print("\n[Expected Script]")
                print(script)
                print("\nContinue entering your answer.")
                continue

            if command == "/next":
                break

            if command == "/end":
                correct = grade("\n".join(lines), script)

                if correct:
                    break

                print(
                    "\nEnter: Try again | 1: Show script "
                    "| 2: Next | 3: Exit"
                )

                while True:
                    choice = input("> ").strip()

                    if choice in ("", "1", "2", "3"):
                        break

                    print("Press Enter or type 1, 2, or 3.")

                if choice == "3":
                    print("Quiz ended.")
                    return

                if choice == "2":
                    break

                if choice == "1":
                    print("\n[Expected Script]")
                    print(script)

                lines = []
                print("\nEnter your answer again from the beginning.")
                continue

            lines.append(line)

        index = (index + 1) % len(QUESTIONS)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nQuiz ended.")