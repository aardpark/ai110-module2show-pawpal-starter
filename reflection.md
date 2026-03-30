# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

So the uml design is for a standard CRUD scheduler. We're starting bottom up, ownership of the task is the pet. pet is the owner. then owner is the scheduler. This allows for a natural hierarchy where each parent can have multiple children all the way down. 

Scheduler - assigned responsibilities having to do with timing, conflicts, scheduling. 

Owner - assigned responsibilities regarding pet ownership.

pets - assigned responsibilities regarding tasks and identity of the pet. 

tasks - assigned responsibilities regarding task information, priority, frequency, etc.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, we needed to change implementation of how add task was added when it came to conflicts. before it would throw an error but still get added to the schedule - obviously not intended behavior. We changed it so that if there was a time conflict, it would block the added task completely while throwing an error.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?


So for constraints the primary constraint had to be time. we organize by chronological order, earliest first. 
priority stored on every task but we defer to time for sorting currently. I decided on time as the primary constraint because when you're looking at a schedule, it only makes sense to organize chronologically first, but I also added an option to sort by priority as well. 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler had to choose between priority first or time first. we ended up being able to do both, but the primary view is time based. I think it's reasonable because for information, time is more immediately useful for a scheduling app.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

AI was extremely helpful in getting situated, distilling instructions down to the most fundamental and important sequence, keeping track of requirements that I had forgotten about, acting as a good reference for the instructions, etc. 

First, I identified the most likely structure of the final project required, then I discussed with the AI the best steps to get to that final structure. I attempted to bypass any pain points by seeing what the final project would look like, and working backwards from there, rather than just slapping on requirements as we went. 

The most useful prompts were questions regarding implementations, and using questions to help lead the AI to the final design of the project/intended use cases of the classes.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One ai design suggestion I pushed back on was not showing completed tasks. completed tasks are useful for a variety of reasons, so I modified the suggestion to add a boolean field to the task, and adding a different ui styling for completed events. it's useful to see completed events for a multitude of reasons, including verification of systems working, and gamification within the app itself - people like feeling like they're accomplishing something. 

I evaluated it by asking my AI to provide code diffs, and following chains of logic to determine which design decisions were related to which parts of the code. Then I asked for an explanation of that specific part.

---



## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Every time we added new functionality, we would add a new test to check its intended function. Most of the tests simply checked to make sure that adding or removing or editing values worked properly. Some checked for behavior when given incorrect inputs. These tests were important because they let me know what's going on with the behavior of the code before I have to test it thoroughly by launching the app. it saves time and effort before I jump into human testing.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

4/5. I'd be more confident if I had more people beta testing and giving feedback. 

As far as edge cases, I think if I had more time I would really test adding and removing logic for tasks and pets. Since pets are a lifelong commitment, you'd want an app that can handle many many operations over the course of operation without breaking due to unexpected behavior.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

very satisfied with the AI's ability to package requirements concisely. It removes all of the friction of the non-engineering aspects.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had to do it again, I would start by thinking of what the ui should look like, then think about how the back end could fit that need. That would be a UX first approach, which I think would have been less work.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Even if the plan going in is good, you will need to remain flexible when it comes to individual implementations of features. AI can't really comprehend front end and back end together, often creating good backend systems while forgetting to wire it up properly with the front end. 
