from services.db import db

def validate_fields(nome, cidade, capacidade):
    nome   = nome.strip()   if nome   else ''
    cidade = cidade.strip() if cidade else ''

    if not nome:
        return 'Nome é de preenchimento obrigatório'
    if not cidade:
        return 'Cidade é de preenchimento obrigatório'
    if not capacidade:
        return 'Capacidade é de preenchimento obrigatório'
    else:
        try:
            capacidade = int(capacidade)

            if capacidade <= 0:
                return 'Capacidade deve ser um número maior que zero'
        except ValueError:
            return 'Capacidade deve ser um número válido'
    
    return None


def validate_id(station_id):
    try:
        station_id = int(station_id)
    except ValueError:
        return 'ID da estação deve ser um número válido'

    return None

class Estacao(db.Model):
    id         = db.Column(db.Integer,     primary_key=True)
    nome       = db.Column(db.String(100), nullable=False, unique=True)
    cidade     = db.Column(db.String(100), nullable=False, unique=True)
    capacidade = db.Column(db.Integer,     nullable=False)


    @classmethod
    def add(cls, nome, cidade, capacidade):
        error_message = validate_fields(nome, cidade, capacidade)

        if error_message:
            print(f'[ERRO] Adicionar estação: {error_message}')
            return None, error_message

        new_station = cls(nome=nome, cidade=cidade, capacidade=capacidade)

        if not new_station:
            print(f'[ERRO] Adicionar estação: Erro ao instanciar novo objeto estação')
            return None, error_message
        
        try:
            db.session.add(new_station)
            db.session.commit()
            print(f'[SUCESSO] Adicionar nova estação: {new_station}')
        except Exception as e:
            print(f'[ERRO] Adicionar nova estação: {e}')
            db.session.rollback()
            return None, str(e)
        
        return new_station, None


    @classmethod
    def get(cls):
        return cls.query.all()
    

    @classmethod
    def get_by_id(cls, station_id):
        error_message = validate_id(station_id)

        if error_message:
            print(f'[ERRO] Buscar estação por ID: {error_message}')
            return None, error_message

        return cls.query.get(station_id), None
    

    @classmethod
    def update(cls, nome, cidade, capacidade, station_id):
        error_message = validate_id(station_id)

        if error_message:
            print(f'[ERRO] Atualizar estação por ID: {error_message}')
            return None, error_message

        station_db = cls.query.get(station_id)

        if not station_db:
            error_message = '[ERRO] Atualizar estação por ID: ID da estação não existe'
            print(error_message)
            return None, error_message

        error_message = validate_fields(nome, cidade, capacidade)

        if error_message:
            print(f'[ERRO] Atualizar estação por ID: {error_message}')
            return None, error_message

        station_db.nome      = nome
        station_db.cidade    = cidade
        station_db.capcidade = capacidade

        db.session.commit()
        print(f'[SUCESSO] Atualizar estação por ID: {station_db}')

        return station_db, None


    @classmethod
    def remove_by_id(cls, station_id):
        error_message = validate_id(station_id)

        if error_message:
            print(f'[ERRO] Remover estação por ID: {error_message}')
            return None, error_message

        station_db = cls.query.get(station_id)

        if not station_db:
            error_message = '[ERRO] Remover estação por ID: ID da estação não existe'
            print(error_message)
            return None, error_message
        
        db.session.delete(station_db)
        db.session.commit()
        print(f'[SUCESSO] Remover estação por ID: {station_db}')
        
        return station_db, None