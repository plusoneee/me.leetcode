## YAML

### Notes
- Dictionary: Unordered.
- List: Ordered.
- Hash(#): Comments.

### Key Value Pair
* Remember must have a `space` followed by a column. Differentiating the `key` and the `value`.
```yaml
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken
```

### Array/ List
* The `Key` followed by a column on the next line enter each item with a `dash` in the front. The `dash` indicates that it's an elemnt of an array.
```yaml
Fruit:
    - Orange
    - Apple
    - Banana
Vegetables:
    - Carrot
    - Cauliflower
    - Tomato
```
* The order of items matter the list shown are not the same:
```yaml
Fruits:
    - Orange
    - Apple
    - Banana
```
Not equal to 
```yaml
Fruits:
    - Apple
    - Orange
    - Banana
```

### Dictionary/ Map
* Must have `equal number of blank spaces` before the properties of a single item (all aligned together). 
```yaml
Banana:
    Calories: 105
    Fat: 0.4g
    Carbs: 27g
Grapes:
    Calories: 62
    Fat: 0.3g
    Carbs: 16g
```

### Example
#### Eaxmple 01
A list of fruits and the elements of the list are banana and grape.
* YAML:
```yaml
Fruits:
    - Banana:
        Calories: 105
        Fat: 0.4
        Carbs: 27
    - Grapes:
        Calories: 62
        Fat: 0.3g
        Carbs: 16
```
* Json:
```json
{
  "Fruits": [
    {
      "Banana": {
        "Carbs": 27, 
        "Calories": 105, 
        "Fat": 0.4
      }
    }, 
    {
      "Grapes": {
        "Carbs": 16, 
        "Calories": 62, 
        "Fat": 0.3
      }
    }
  ]
}
```
#### Eaxmple 02
* YAML
```yaml
Employee:
  Name: Jacob
  Sex: Male
  Age: 30
  Title: Systems Engineer
  Projects:
    - Automation
    - Support
  Payslips:
    - 
        Month: June
        Wage: 4000
    - 
        Month: July
        Wage: 4500
    -   
        Month: August
        Wage: 4000
```
* Json:
```json
{
  "Employee": {
    "Name": "Jacob", 
    "Age": 30, 
    "Sex": "Male",    
    "Projects": [
      "Automation", 
      "Support"
    ], 
    "Title": "Systems Engineer", 
    "Payslips": [
      {
        "Wage": 4000, 
        "Month": "June"
      }, 
      {
        "Wage": 4500, 
        "Month": "July"
      }, 
      {
        "Wage": 4000, 
        "Month": "August"
      }
    ], 
  }
}
```