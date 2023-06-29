import openai

openai.api_base = "http://localhost:8080/openai"
openai.api_key = "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"

# prompt = """<|im_start|>system
# A conversation between a user and an LLM-based AI assistant. The assistant gives helpful, honest, and convcise answers.

# The user is generating out a work order for building ships. Given the following input:

# "Create a new weld at site A7-B1"

# The user expects the following return format in JSON without any other information:

# {"action": "create", "task": "weld", "site": "A7-B1"}
# <|im_end|>
# <|im_start|>user
# I need someone to go down and x-ray the pipe installation at site LAN-A1-B4
# <|im_end|>
# <|im_start|>assistant
# """

prompt = """<|im_start|>system
# Learn SudoLang

SudoLang is a pseudolanguage designed for interacting with LLMs. It provides a user-friendly interface that combines natural language expressions with simple programming constructs, making it easy to use for both novice and experienced programmers.

SudoLang can be used to produce AI-first programs such as chatbots and text-based productivity applications, or to produce traditional code in any language using AI Driven Development and the `transpile` function.

SudoLang is designed to be understood by LLMs without any special prompting. An AI model does not need the SudoLang specification to correctly interpret SudoLang programs.

## Why?

Save 20% - 30% tokens over natural language prompts, with more predictable output, conforming to data structures you supply.

Author traditional code in SudoLang and transpile to any language for 10x - 20x productivity by having the language model automatically build functions, algorithms, unit tests, etc.

Main features:

* Markdown - freely mix documentation and code.
* Interfaces encapsulate related state, constraints, `/commands`, and functions.
* Declarative, natural language constraints.
* /commands that can be inferred automatically.
* Pipe operator `|>` for function composition.
* Most operators you use in any popular programming language. (Exception: use `^` for exponentiation instead of `**`. Use `xor` for XOR).
* Pattern matching with inferred patterns and destructuring.
* Function modifiers to customize function behaviors, inference style, length, output format, etc. e.g. `list(5 pizza toppings):format=yaml`
* Loops and block scopes.
* Transpile to any language.

## Constraint based programming in SudoLang

Simple natural language constraints can represent complex behaviors with little human readable definitions, requirements, and rules.

```
function longestIncreasingSubsequence() {
  A subsequence is derived from the original sequence by selectively omitting elements without changing the order.
}
```

This also works for math axioms:

```
function pythagoreanTipple() {
  if not supplied, generate random seeds
  a^2 + b^2 = c^2
  return [a, b, c]
}
```

## Interfaces

Define interfaces with the optional interface keyword, or omit it:

```
Foo {
  bar // undefined
  baz: "Default value"

  Constraints {
    // list constraints in natural language
    // can be used to dynamically synchronize state, emit events, etc
    when baz changes, increment bar and emit({ changed: baz, oldValue, newValue })
  }
  log() {
    { bar, baz } as json
  }
}
```

Because it's an LLM, many functions can be automagically inferred. Just call a function with a descriptive name without defining it, and it will usually work.

---

# SudoLang in a Nutshell

Roleplay as a tutor teaching SudoLang, following the instructions below:

```
ConstraintExample1 {
  /*
  Requirements are a special kind of constraint that throw errors when the user tries to perform an invalid action. Requirements are constraints on inputs.

  Imagine you're building a scheduling app for a conference. You have 4 stages. You need to ensure that you don't book more than 4 speakers in the same timeslot. Here's how you might do that:
    */
  State {
      Stages [1,2,3,4]
  }
  Constraints {
        Require the number of overlapping speaker timeslots to be less than the number of available stages.
    }
}

ChatbotConstraintExample {
  /* Output constraints tell the AI how to constrain its output, rather than constraining user inputs. For example, if you want a chatbot to use a young adult vocabulary: */
  Constraints {
    Avoid mentioning constraints.
    Vocabulary: Young adult
    Tone: Playful.
     Use emojis when it's fun.
    Use *emotes* for fun.
  }
}

Scoreboard {
  /* Constraints can also be used to synchronize state */
  State {
    Score
  }
  Constraints {
    Increment score with each correct user answer.
   }
}

SudoLangInANutshell {
  Scoreboard
  Lessons [
    What is SudoLang?:
      SudoLang is a pseudocode programming language that combines the freedom and ease of use of natural language with the sound structure of block scopes, functions, variables, and constraint-based programming. It's easy to learn and use, and all sufficiently advanced language models understand it without any special prompting.
   
    Features:
      Constraint-based programming using constraints to guide AI outputs (rather than user inputs), and keep state in synch automatically with constraint solvers.
      Pattern matching with semantic matching.
      Function composition with the pipe operator: `|>`
      If expressions
      Supports all common programming language and math operators.
    
    Anatomy:
      A typical SudoLang program consists of:
        Preamble - The program title followed by a one-paragraph introduction. It usually takes the form "Roleplay as [expertise]. Your job is to [short job description] by following the instructions:"
      Supporting functions or interfaces
      Main interface - Typically consists of state, constraints, methods and/or commands
      Initializer - a first command or action to kick the program off.
    
    Constraints:
      Constraint based programming allows you to define relationships between different parts of the state that are automatically kept in-synch by the AI. Think of a constraint as an instruction that guides the output produced by the AI. The best constraints declare what you want rather than spell out step-by-step how to do it. For example, you can make a constraint that says all employees must be paid a minimum salary, and define a solver that automatically awards raises as needed if you raise the minimum salary.
    ]
  /v | vocab - Vocabulary review
  /f | flashcards - Play the vocab flashcard game
  /c | challenge - Get a SudoLang coding challenge
  /e | expand [topic] - Get a deeper explanation of the given topic
  /l | lessons - Show lesson list
  /s | score - Show student score
  /h | help - List these commands
}

welcome()

/help
```<|im_end|>
<|im_start|>user
/help
<|im_start|>assistant
"""


response = openai.Completion.create(
    # model="text-davinci-003",
    model="ctransformers",
    prompt=prompt,
    max_tokens=2048,
    temperature=0.01,
    context_length=4096,
    stream=True,  # this time, we set stream=True,
)

for event in response:
    print(event.choices[0].text, end="", flush=True)
print("\n")
