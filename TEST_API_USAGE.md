# Test Student API Commands

## Using curl:
```bash
# Test with student ID 4402080
curl -X GET "http://localhost:8000/api/registration/students/test/" \
  -H "Content-Type: application/json" \
  -H "X-Student-ID: 4402080"

# Test with invalid ID
curl -X GET "http://localhost:8000/api/registration/students/test/" \
  -H "Content-Type: application/json" \
  -H "X-Student-ID: 999999"

# Test without header
curl -X GET "http://localhost:8000/api/registration/students/test/" \
  -H "Content-Type: application/json"
```

## Using JavaScript fetch:
```javascript
// Test API call
fetch('/api/registration/students/test/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-Student-ID': '4402080'
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## API Endpoint:
- **URL**: `/api/registration/students/test/`
- **Method**: GET
- **Header Required**: `X-Student-ID: {student_id}`
- **Response**: JSON with student data from student_basic table

## Test in Browser:
Open `test_student_api.html` in your browser to test the API with a UI.

## Example Response:
```json
{
    "success": true,
    "message": "Student data fetched successfully for ID: 4402080",
    "data": {
        "id": 4402080,
        "student_name_bn": "John Doe",
        "student_name_ar": "",
        "student_name_en": "",
        "father_name_bn": "Father Name",
        "roll_no": 123,
        "reg_no": 456789,
        "year": 2024,
        "status": "active",
        // ... other fields
    }
}
```