---
name: skill_tractate
description: Work on Tractatus Principatuum — iron dictated speech into numbered propositions, probe the author for analogies and clarifications, or scan the tractate for citations and logic. Load before editing tractate.md, minting STT into tractate form, or discussing a claim in that file.
---

# Tractate work

The work lives in `Tractatus Principatuum/`. The page is `tractate.md`. `todo.md` is the author's plan for sections not yet written. `citations.md` is external reading, not a proposition index.

This is statement work. Continuous-prose habits do not transfer. The page is the corpus.

## Rules are not optional

Before any sentence is proposed, placed, or rewritten, read `.insula/rules/writing.md` in full in this turn. Not a range. Not the cadence section. The file. If that read has not happened in this turn, do not draft. Do not edit `tractate.md`. Do not answer a voice question from memory of the rules.

Read `.insula/rules/dictation.md` in full in this turn when the input is speech-to-text, a transcript, or a voice dump. Ironing and rephrasing are different jobs. Do not mix them. Do not read it "just in case" on an essay and then treat that as having done the writing rules.

If those files and this skill conflict, the rules win on voice and cadence. This skill wins on tractate form and on which job is being done.

A draft written without that read is a failed draft even if the sentences look fine. Delete it and start over after the read. Do not patch the one line the user caught and call the rest compliant.

## Reddit writing

The author will call this "reddit writing." They loathe it. Treat that phrase, and any cousin of it ("bot language," "the beat," "the punch"), as a hard fail of the draft in front of you, not as a style note to nod at and then keep.

Reddit writing is the sound of a post that is performing a thought instead of having one. The setup, the turn, the little landing. A claim that pauses so the reader can feel how it landed. A sentence whose only job is to be the button on the previous sentence.

It shows up as:

- The beat, then the punch. A long sentence, then a short one that only restates it cleaner. "That is the whole relation." "It is not." "That is the point." "Full stop."
- The turn. "It's not X, it's Y." "The question isn't X. The question is Y." "Not because A. Because B." "X isn't the exception. It's the rule."
- The button. A fragment after a real sentence, set there so the line can be screenshotted.
- The stack. "It's about X. It's about Y. It's about Z." Three items because three feels like an argument.
- The throat-clear. "Here's the thing." "The real X is." "And that's the part nobody wants to say." "Let that sit."
- The clever noun doing the work the mechanism should do. If the sentence still works after the fashion word is cut, the fashion word was the punch. Cut it.

A proposition does not land. It states, and it cites, and it stops. If a draft has a sentence you could lift as the last line of a post, that sentence is the failure. Delete it. Do not replace it with a quieter version of the same landing.

Before handing anything back, read the draft as if it were a comment under a thread. If you can hear the upvote, rewrite. The banned-cadence list in writing.md is the grep. This section is the reason it applies twice as hard here. One accidental contrast in the author's own source can stay, because it was theirs. A contrast the model reached for is already the habit. Kill it even once.

## Orient

Before proposing, placing, or checking a claim:

1. Read the section the user is in, plus the propositions they name.
2. If they did not name a number, search `tractate.md` for the local nouns before inventing a location.
3. Skim `todo.md` only when the job is a section that is not on the page yet. Do not import its essay voice into a proposition.
4. Note the numbering already in use. Do not renumber a placed proposition unless asked.

## Voice of the page

Extract from `tractate.md`, not from a portrait and not from `todo.md`.

- First person. "I think," "I notice," "I will call it." Rare "we," and only for a term being named, not a lectern.
- One claim per integer. Bold number, then the sentence or two that do that claim's job. A subpoint specifies. It does not restate the parent in a new metaphor.
- Cross-cites are part of the grammar: `(4.32)`, `6.16`, `the way 3.3 describes`, `By 5.151`. Cite a number that is on the page. Do not cite a number you are about to invent.
- A number is a marker, not a speaker. When a mint or a rephrase asks for the justification to be embedded, work the number into the clause (`the remnant across a gap (7.1)`) or set it parenthetically at the point it justifies. Do not hand the number a verb: "7.4 states that," "4.34 already said," "11.3 just named," "9.132 wants." Nobody talks that way, and the page does not either. If the sentence only exists to report what the other number said, the sentence is the failure. Fold the number in and let the claim stand on its own.
- Local nouns stay local once named: principality, remnant, soft system, hard system, weight, emotional landscape, singularity, flame, fathom, chosen, placed, mitigation. Do not rotate them through synonyms. Do not upgrade them.
- Analogies are one move, then a return. Temperature, bone, towns. The likeness is held as likeness. 4.341 is the failure mode: likeness treated as readable identity.
- Register jumps without a gear-change sentence. A stiff term can sit next to "sort of" or "I don't think."
- Endings are the claim, not a moral. No kicker. No "put together." No last integer that recaps the section.
- Straight quotes. Parentheses for cites and asides. Em dashes are rare. Backticks mark a term being installed (`weight`, `chosen`), not code.
- Spelling and agreement follow the page, including slips the page already keeps. Do not normalize toward edited English.

Section heads on the page are inconsistent (`##` and `#`). Match the nearest head. Do not restyle the file.

## Jobs

Decide the job before touching sentences. Say which one you are in, in a short line, then do it. Do not do two at once unless the user asked for both.

### Iron

Signal: speech-to-text, transcript, dictation, "clean this up," a paste that still sounds spoken, recognition garbage.

The user is often already in the middle of rephrasing. Ironing is the first pass, not the finished proposition.

1. Follow dictation.md. Restore the token. Leave the clause, the order, the hedge, the self-correction.
2. Show the ironed speech. Do not silently turn it into a proposition.
3. Mark any stretch you cannot restore. Do not supply the sentence they must have meant.
4. If they then ask to put it on the page, that is a second job: rephrase into tractate form. Extract the points. Discard the spoken skeleton. Write the claim in the page's voice, one job per integer.
5. During that second job, propose the number and where it sits. Do not insert it until they say to. When they do, edit only that span. Do not tidy neighbors.

Rephrasing before the iron is done will bake the recognizer's sentence into the tractate. Do not.

### Probe

Signal: "what do you think," "does this hold," "help me find the analogy," discussion with no request to write the page.

The user is the source. The agent is not a co-author and not a lecturer.

1. Read the propositions the question sits on. Answer from those, not from a general philosophy survey.
2. Ask for the analogy or the clarification you actually need. One or two questions. Name the gap: which numeral is doing the work, what the likeness is being asked to carry, what would count as the claim failing.
3. Offer a candidate analogy only as a candidate, in their nouns, and say what it would commit them to. Do not install it.
4. If they are working a thought aloud, reflect the claim back shorter than they said it, then ask. Do not produce the proposition unless they ask for tractate form.
5. Do not close the discussion with a synthesis paragraph.

### Scan

Signal: "where did I say," "cite the place," "check this against," "does this contradict," a request to find a location or test a chain.

1. Search `tractate.md`. Return the numbers, and a short quote only long enough to show why that number is the one. Do not paste whole sections back.
2. If several numbers could be the cite, list them and say what each one actually claims. Let them pick.
3. A logic check names the chain: which numeral depends on which, and where the step is not on the page. Do not repair the chain by writing new propositions into the file.
4. A missing step can be stated as a missing step. Writing it is a different job, and only if they ask.
5. `todo.md` and `citations.md` are not evidence that a claim is already in the tractate. Say so if the only hit is there.

## Placement

- New claim: next free integer in the section, or a new decimal under the parent it specifies. Do not insert a number between two placed ones by shifting the rest.
- A section that does not exist yet: look at `todo.md` for the intended order. Write propositions only. Leave the planning prose in `todo.md`.
- Stop when the asked claim is on the page. Do not add the next integer, the next section, or a closer.

## Verify

Before handing back written propositions:

- One job per integer. No slogan. No reddit writing: no beat-then-punch, no turn, no button, no stack of three. Grep the draft against the banned cadences in writing.md. If a line could close a post, it does not go on the page.
- Every parenthetical number exists in `tractate.md`. No number is the subject of a reporting verb. "X.XX states that," "already said," "just named," "wants" are the failure even once. The number sits in the clause or in parentheses.
- No new noun where the page already has one.
- The likeness is still a likeness, unless they explicitly asked to cross 4.341.
- Source speech, if any, was ironed before it was rephrased, and the two passes were not collapsed.
