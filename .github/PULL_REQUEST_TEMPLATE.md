Pull request for #PULL_REQUEST_ID

# Development checklist (To be completed by main developer)

- [ ] Code is working as expected
- [ ] Acceptance criteria met
- [ ] Passes coding standards
- [ ] Unit tests written and passing
- [ ] PR open and linked to issue
- [ ] PR using correct template
- [ ] Issue closed
- [ ] A quick self code review performed


# Code Review Checklist
## Code
 - No syntax/runtime errors and warnings in the code
 - No deprecated functions in the code
 - “Dead Code” should be removed. If it is a temporary hack, it should be identified as such.
 - All code follows coding standard (ESLint - http://eslint.org/docs/rules/)
 - No magic numbers. All numbers (that has no clear origin should be defined as a variable).
 
- [ ] Above criteria met

## Documentation
 - All methods are commented in clear language. If it is unclear to the reader, it is unclear to the user.
 - All class, variable, and method modifiers should be examined for correctness.
 - Describe behaviour for known input corner-cases.
 - Complex algorithms should be explained with references. For example,  document the reference that identifies the equation, formula, or pattern. In all cases, examine the algorithm and determine if it can be simplified.
 - Incomplete code is marked with `//TODO` or `//FIXME` markers.
 - All public and private APIs are examined for updates.

- [ ] Above criteria met

## Unit Tests
 - Unit tests are added for each code path, and behaviour.
 - Unit tests must cover error conditions and invalid parameter cases.
 - Unit tests for standard algorithms should be examined against the standard for expected results.
 - Ensure that the code fixes the issue, or implements the requirement, and that the unit test confirms it. If the unit test confirms a fix for issue, add the issue number to the doc block.
 - Unit tests must have assertions
 - Regression tests for fixes are included.
 - As a reviewer, you should understand the code. If you don’t, the review may not be complete, or the code may not be well commented.

- [ ] Above criteria met

## Error Handling
 - Invalid parameter values are handled properly early in methods (Fast Fail/Return Early).
 - **Don't swallow exceptions!** You should at least log the exception.

- [ ] Above criteria met

# Testing checklist

- [ ] All unit tests pass
- [ ] All acceptance criteria are met and working as expected
- [ ] Spot checks have been performed on existing functionality that may have been affected
