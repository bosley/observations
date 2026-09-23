---
description: Mint speech-to-text and voice dumps into readable prose without rephrasing the description.
globs: "**/*.md"
alwaysApply: false
---


These rules govern any model that writes, rewrites, expands, or cleans prose. They are not tied to an editor, a repo, or a project layout. They do not apply to code, commit messages, or other non-prose artifacts.

Do not sound like a default assistant. Do not sound like a published essay unless the surrounding text already does. Write like a person thinking on the page: uneven, specific, willing to leave a seam. If the surrounding text has a different habit, that habit wins.

## Scope

- Named samples, attached files, and folder-local instructions outrank this document.
- When the user names an output, write there. Leave the source alone unless they say overwrite.
- Stop when the asked claim is on the page. Do not add the next section, the next integer, or a closer they did not ask for.

## Modes

Decide the job before touching sentences. Reforming cadence in place will not fix a page whose skeleton is already essay-shaped. That job is translation.

| Mode | Signal | Procedure |
|---|---|---|
| Reform | slop, un-AI, rewrite, tighten, de-GPT | Keep the claims and the facts. Kill the cadence. Do not add new thesis sentences. |
| Translate | minted from discussion, "drive the same point", rewrite entirely, "I just want the point out" | The source already sounds like writing. Extract the points. Discard the skeleton. Write a new page in the extracted voice. Same claims, new bones. |
| Mint | speech-to-text, transcript, dictation, voice dump, talking through a subject | Iron recognition errors back into what was said. Do not rephrase the description. See the dictated-description use case. |
| New | outline, notes, "write this", continue a draft | Write in the voice extracted from the surrounding text. |
| Statements | "statement", numbered claims | Numbered nested claims. One job per integer. Match statement files already beside the work. Continuous prose is the wrong sample. |

## Idiolect extraction

Voice is not stored in an examples folder and is not a fixed portrait of one writer. It is recovered, at the time of writing, from the text that already surrounds the job: the file being edited, sibling files in the same folder, and any passage the user names or attaches. If those conflict, the named passage wins, then the file in hand, then the nearest sibling.

Treat that corpus as the sole evidence. Do not import a generic "human" style, and do not "correct" the corpus toward standard edited English.

The extraction is a descriptive analysis of an idiolect, not a rewrite of it. Read for recurrent formal features and copy those features. Do not summarize the writer's "personality."

**Graphological and orthographic features.** Spelling that recurs. Agreement that recurs. `its` / `it's` as the corpus actually mixes them. Capitalization, including a mid-sentence lowercase `i` if it is there. Quotation marks: straight or curly, closed or left open. Whether a pause is a comma, a parenthesis, or a dash. Whether backticks are used as homemade term-marks rather than as code. Unclosed quotes and leftover oral grammar stay if they were already there. Idiosyncrasy in the corpus is data. When the source is the user's (mint, reform, clean-up), do not normalize spelling, agreement, or pronoun forms.

**Syntactic features.** Mean and variance of sentence length. Coordination with `and` / `but` versus subordination. Whether a short sentence opens or closes a block, or sits as a slogan in the middle. Tense that slips and stays. Stiff grammar set next to talk (`I knew not…`). Hedges as ordinary asides, after which the sentence continues. Whether a ranking, once started, is walked back in the same breath.

**Lexical features.** Pair-nouns and local terms, named once and then used, not rotated through synonyms. Register jump: a concrete local noun set beside a stiff or technical one, with no gear-change sentence between them. Do not pick "plain" or "philosophical" and stay there. Contractions, fillers, and hedges if the corpus keeps them. Do not upgrade vocabulary.

**Discursive and pragmatic features.** Person: talk *from* I when the corpus does. Direct address is rare unless the corpus uses it. Role-as-camera (`As a parent I…`) is not a lectern "we." How a claim is staged: scene first, question from inside the scene, rather than a definition up front. Analogy as a move — same shape, different field — then one explicit return (`So, back to…`). Distinctions the corpus bothers to name, it names. It does not restate the distinction as a closer. Warmth where the example is small. Dryness where an adult is incompetent. No sermon after the feeling.

**Textual features.** Paragraph length varies with the thought. Subheads and bullets appear only if the surrounding text uses them. Openings sit on hands and place when that is the corpus habit. Endings are quieter than the middle. A short last line may sit slightly balanced. Do not add a moral paragraph after it.

When generating new prose in an extracted voice: copy the grammar moves, the register jump, the marks, and the scene-then-return if those are what the corpus does. Do not spray fake typos as costume. A light echo of a recurrent mark is enough once the syntax and the diction already match. Do not invent fingerprint the corpus does not have.

Continuous-prose features do not transfer into statements. Statement voice is extracted only from other statement files beside the work.

For dictated description, extraction is also the pronunciation lexicon. The surrounding text tells you which word the recognizer should have printed. It does not license a cleaner sentence than the one that was spoken.

## Use case: speech-to-text while describing a subject

A frequent job: the user dictates while describing a subject. A text in front of them, an object, a mechanism, a scene, a claim they are walking around. They point, qualify, back up, rename the part, say "no, the other one." They are not composing a page. Speech-to-text then writes a second text on top of that speech, and the second text is full of the software's mistakes.

The job is to iron those mistakes back into the speaker's voice. Ironing is local. Rephrasing is a different job, and it is the wrong one here.

**What counts as an aberration.** A recognition error, not a weak thought and not a sentence that needs editing.

- Phonetic substitution. The recognizer maps the sound onto the nearest word it has. A name, a technical noun, or an in-house term comes out as a common word with a similar mouth-shape. "Insula" as "in sula" or "insular." A term of art as a kitchen word.
- Homophone and near-homophone swap. Their/there, principle/principal, and the domain pair that only the subject can split.
- Segmentation. One word split, two words fused, a boundary moved so a modifier sticks to the wrong noun.
- Function words dropped or invented. Small words the model was unsure of, guessed.
- No lexicon entry. A proper noun or a private term spelled as a phonetic guess, or replaced by a frequent word.
- Recognizer punctuation and casing. The clause cut in the wrong place, so the grammar says something the speech did not.
- Helpful substitution. The software picked a cleaner synonym, or smoothed a restart into a grammatical sentence that was not said. That smoothing is still an aberration.

**How to iron one.**

1. Read the bad token as sound. Ask what was likely pronounced. Do not ask what a writer would have written about the subject.
2. Test the candidate against the subject under description and against words already in the surrounding text. That text is the lexicon. A restoration the phonetics do not force, and that the lexicon does not have, is a rephrase.
3. If the user already has a name for the thing, restore that name. Do not promote it to the textbook term unless the sound is the textbook term.
4. Once the word is identified, spell and inflect it the way the surrounding text does, including `its` / `it's` and agreement. Standard English is not the target. Their voice is.
5. If two restorations fit the sound, take the one closer to diction already on the page. Not the more precise one. Not the more impressive one.
6. Change the token, the boundary, or the bad mark. Leave the clause. Leave the order. Leave the hedge, the deixis, the "sort of," the self-correction.
7. If no candidate fits both the sound and the subject, mark the stretch. Do not supply the sentence they must have meant.

**Ironing versus rephrasing.** You have started rephrasing when you touch a stretch that was already a possible hearing. Upgrading "sort of the joint" to "the articulation." Turning the order they noticed the