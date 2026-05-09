# MicTest12-1.0 API Reference

Complete API documentation for MicTest12-1.0 framework.

## Table of Contents

- [Core API](#core-api)
- [Test Runners](#test-runners)
- [Assertions](#assertions)
- [Mocking & Spying](#mocking--spying)
- [Lifecycle Hooks](#lifecycle-hooks)
- [Utilities](#utilities)

## Core API

### describe(name, callback)

Create a test suite.

**Parameters:**

- `name` (string): Description of the test suite
- `callback` (function): Function containing test cases

**Example:**

```javascript
describe('User Module', () => {
  // test cases here
});
```

### it(name, callback)

Define a single test case.

**Parameters:**

- `name` (string): Description of what should happen
- `callback` (function): Test implementation

**Example:**

```javascript
it('should create a new user', () => {
  // test code
});
```

### test(name, callback)

Alias for `it()`. Identical functionality.

**Example:**

```javascript
test('should validate email format', () => {
  // test code
});
```

## Test Runners

### npm test

Run all tests in the project.

**Options:**

- `--watch`: Watch mode for development
- `--coverage`: Generate coverage report
- `--bail`: Stop on first test failure
- `--testNamePattern`: Filter tests by pattern

**Examples:**

```bash
npm test
npm test -- --watch
npm test -- --coverage --bail
```

### npm test -- [pattern]

Run tests matching a specific pattern.

**Example:**

```bash
npm test -- user.test.js
npm test -- --testNamePattern="create"
```

## Assertions

### expect(value)

Create an expectation object.

**Chaining methods:**

- `.toBe(expected)`: Strict equality (===)
- `.toEqual(expected)`: Deep equality
- `.toStrictEqual(expected)`: Strict equality including undefined
- `.not`: Negate assertion

**Examples:**

```javascript
expect(5).toBe(5);
expect({ a: 1 }).toEqual({ a: 1 });
expect(value).not.toBe(null);
```

### Truthiness Assertions

Check values for truthiness:

- `.toBeTruthy()`: Passes if value is truthy
- `.toBeFalsy()`: Passes if value is falsy
- `.toBeNull()`: Checks for null
- `.toBeUndefined()`: Checks for undefined
- `.toBeDefined()`: Checks value is defined

**Example:**

```javascript
expect(user).toBeDefined();
expect(error).toBeNull();
```

### Number Assertions

Test numeric values:

- `.toBeGreaterThan(value)`: Larger than
- `.toBeGreaterThanOrEqual(value)`: >= comparison
- `.toBeLessThan(value)`: Smaller than
- `.toBeLessThanOrEqual(value)`: <= comparison
- `.toBeCloseTo(value, decimals)`: Float comparison

**Example:**

```javascript
expect(result).toBeGreaterThan(0);
expect(pi).toBeCloseTo(3.14159, 5);
```

### String Assertions

Test string values:

- `.toMatch(regex)`: Matches regex pattern
- `.toHaveLength(length)`: String length
- `.toContain(substring)`: Contains substring

**Example:**

```javascript
expect(email).toMatch(/^[\w\.-]+@[\w\.-]+\.\w+$/);
expect(name).toHaveLength(5);
```

### Array/Object Assertions

Test collections:

- `.toContain(item)`: Array contains item
- `.toHaveLength(length)`: Length check
- `.toHaveProperty(key)`: Object has property
- `.toMatchObject(object)`: Partial match

**Example:**

```javascript
expect(users).toContain(user);
expect(config).toHaveProperty('apiKey');
expect(response).toMatchObject({ status: 200 });
```

### Exception Assertions

Test error handling:

- `.toThrow()`: Function throws error
- `.toThrow(Error)`: Throws specific error type
- `.toThrow('message')`: Throws with message

**Example:**

```javascript
expect(() => {
  invalidFunction();
}).toThrow(ReferenceError);

expect(validator.checkEmail).toThrow('Invalid email');
```

## Mocking & Spying

### jest.mock(moduleName)

Mock an entire module.

**Example:**

```javascript
jest.mock('./database');

describe('User Service', () => {
  it('should call database', () => {
    userService.getUser(1);
    expect(db.query).toHaveBeenCalled();
  });
});
```

### jest.spyOn(object, method)

Spy on object method without mocking.

**Example:**

```javascript
const spy = jest.spyOn(console, 'log');
console.log('test');
expect(spy).toHaveBeenCalledWith('test');
spy.mockRestore();
```

### jest.fn()

Create a mock function.

**Example:**

```javascript
const mockCallback = jest.fn();
mockCallback('arg1');
expect(mockCallback).toHaveBeenCalledWith('arg1');
```

### Spy Assertions

Common spy assertions:

- `.toHaveBeenCalled()`: Called at least once
- `.toHaveBeenCalledWith(args)`: Called with specific args
- `.toHaveBeenCalledTimes(count)`: Called exact times
- `.toHaveReturnedWith(value)`: Returned value

**Example:**

```javascript
expect(spy).toHaveBeenCalled();
expect(spy).toHaveBeenCalledTimes(2);
expect(spy).toHaveReturnedWith(expected);
```

## Lifecycle Hooks

### beforeEach(callback)

Run before each test in suite.

**Example:**

```javascript
beforeEach(() => {
  setupTestData();
  initializeModule();
});
```

### afterEach(callback)

Run after each test in suite.

**Example:**

```javascript
afterEach(() => {
  cleanupTestData();
  closeConnections();
});
```

### beforeAll(callback)

Run once before all tests in suite.

**Example:**

```javascript
beforeAll(() => {
  startTestServer();
  loadFixtures();
});
```

### afterAll(callback)

Run once after all tests in suite.

**Example:**

```javascript
afterAll(() => {
  stopTestServer();
  closeDatabase();
});
```

## Utilities

### jest.setTimeout(milliseconds)

Set timeout for current test.

**Example:**

```javascript
jest.setTimeout(10000); // 10 seconds for slow test
```

### jest.retryTimes(count)

Retry flaky test multiple times.

**Example:**

```javascript
jest.retryTimes(3);

it('might be flaky', () => {
  // test code
});
```

### jest.useFakeTimers()

Mock system timers.

**Example:**

```javascript
jest.useFakeTimers();
jest.advanceTimersByTime(1000);
jest.useRealTimers();
```

### jest.clearAllMocks()

Reset all mocks between tests.

**Example:**

```javascript
afterEach(() => {
  jest.clearAllMocks();
});
```
