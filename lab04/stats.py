def parse_record(line: str) -> dict:
    parts = line.split(";")
    
    
    if len(parts) != 3:
        raise ValueError(f"Неверное количество полей: {len(parts)}. Ожидается 3.")
    
    city, temp_str, date = parts
    
   
    if not city or not date:
        raise ValueError("Пустой город или дата.")
        
   
    try:
        temp = float(temp_str)
    except ValueError:
        raise ValueError(f"Температура '{temp_str}' не является числом.")
        
    return {"city": city, "temp": temp, "date": date}
