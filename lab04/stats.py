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


def read_valid(lines: list[str]) -> list[dict]:
    valid_records = []
    
    for line in lines:
        if not line:  
            continue
            
        try:
            record = parse_record(line)
            valid_records.append(record)
        except ValueError:
          
            pass
            
    return valid_records
