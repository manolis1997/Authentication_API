import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from Database import DB
from Insert_Struct import *
from Authentication import *
from typing import List, Dict


db = DB()
conn = db.conn
app = FastAPI()


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token_data = {"sub": user["username"]}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/data", response_model=Dict[str, List[Dict[str, str]]])
async def read_data(current_user: dict = Depends(get_current_user)):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Department,Name,CAST(ID AS VARCHAR(10)) AS ID_str,CAST(Salary AS VARCHAR(10)) AS Salary_str FROM Employee") # it want to cast all columns as string
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))
        cursor.close()

        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/record")
async def create_item(employee: Employee, current_user: dict = Depends(get_current_user)):
    try:
        conn.execute(f"INSERT INTO Employee VALUES {(employee.id, employee.name, employee.salary, employee.department)}")
        conn.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"Success": "Success Insert"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    conn.close()
