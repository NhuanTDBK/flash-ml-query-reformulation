from dataclasses import dataclass
from typing import List


@dataclass
class QuestionComponents:
    wh_word: str
    root_verb: str
    subject: str
    objects: List[str]
    modifiers: List[str]


class FastDependencyParser:
    def __init__(self, nlp=None):
        # Load smallest model for speed
        # Common question patterns
        self.wh_patterns = {
            "what": {"definition", "description", "purpose"},
            "when": {"time", "date", "period"},
            "where": {"location", "place", "direction"},
            "who": {"person", "agent", "doer"},
            "why": {"reason", "cause", "purpose"},
            "how": {"method", "manner", "degree"},
        }
        self.nlp = nlp

    def extract_components(self, doc) -> QuestionComponents:
        """Fast extraction of question components using deps"""
        wh_word = ""
        root_verb = ""
        subject = ""
        objects = []
        modifiers = []

        for token in doc:
            if token.dep_ == "ROOT":
                root_verb = token.text
            elif token.tag_.startswith("W"):
                wh_word = token.text.lower()
            elif token.dep_ in ("nsubj", "nsubjpass"):
                subject = token.text
            elif token.dep_ in ("dobj", "pobj", "attr"):
                objects.append(token.text)
            elif token.dep_ in ("advmod", "amod"):
                modifiers.append(token.text)

        return QuestionComponents(
            wh_word=wh_word,
            root_verb=root_verb,
            subject=subject,
            objects=objects,
            modifiers=modifiers,
        )


class DependencyBasedReformulator:
    def __init__(self, nlp):
        self.parser = FastDependencyParser(nlp)

        # Load minimal word vectors for key terms
        self.word_vectors = self._load_minimal_vectors()

    def _load_minimal_vectors(self):
        """Load only essential vectors for question words and common verbs"""
        return {
            # Question words and similar terms
            "what": ["define", "explain", "describe"],
            "when": ["time", "date", "period"],
            "where": ["location", "place", "area"],
            "who": ["person", "individual"],
            # Common verbs and alternatives
            "is": ["was", "are", "exists"],
            "do": ["does", "did", "perform"],
            "has": ["have", "had", "possess"],
        }

    def reformulate(self, query: str) -> List[str]:
        # 1. Parse query (~5ms)
        doc = self.parser.nlp(query)
        components = self.parser.extract_components(doc)

        # 2. Generate structural variations (~2ms)
        base_variations = self._generate_structural_variations(components)

        return base_variations

        # 3. Apply word substitutions (~2ms)
        semantic_variations = self._apply_word_substitutions(base_variations)

        return list(set(semantic_variations))[:2]

    def _generate_structural_variations(self, comp: QuestionComponents) -> List[str]:
        """Generate variations based on dependency structure"""
        variations = []

        # Basic structure patterns
        if comp.wh_word == "what":
            if comp.root_verb in ("is", "are"):
                # Definition pattern
                variations.extend(
                    [
                        f"{comp.subject} definition",
                        f"{comp.subject} meaning",
                        f"{comp.subject} explanation",
                        f"{comp.subject} basics",
                    ]
                )
            else:
                # Action pattern
                variations.append(f"{comp.root_verb} {' '.join(comp.objects)}")

        elif comp.wh_word == "when":
            # Temporal patterns
            event = " ".join([comp.subject, comp.root_verb])
            variations.extend([f"time of {event}", f"date of {event}"])

        elif comp.wh_word == "where":
            # Location patterns
            entity = comp.subject
            variations.extend([f"location of {entity}", f"find {entity}"])
        elif comp.wh_word == "who":
            # Person patterns
            action = " ".join([comp.root_verb, comp.objects[-1]])
            variations.extend([f"{action}"])
        else:
            variations.extend(
                [
                    f"{comp.subject} {comp.root_verb} {' '.join(comp.objects)}",
                ]
            )

        return variations

    def _apply_word_substitutions(self, variations: List[str]) -> List[str]:
        """Apply word vector based substitutions"""
        result = set()

        for var in variations:
            words = var.split()
            for i, word in enumerate(words):
                if word in self.word_vectors:
                    for similar in self.word_vectors[word]:
                        new_words = words.copy()
                        new_words[i] = similar
                        result.add(" ".join(new_words))

        return list(result)
