# Leads

## POST /leads

Registra um novo Lead no banco de dados.

Modelo de requisição:

```python
{
    "name": "John Doe",
    "email": "john@email.com",
    "phone": "(41)90000-0000"
}
```

`creation_date` e `last_visit` são preenchidos no momento da criação do Lead.

Modelo de resposta:

```python
{
    "name": "John Doe",
    "email": "john@email.com",
    "phone": "(41)90000-0000",
    "creation_date": "Fri, 10 Sep 2021 17:53:25 GMT",
    "last_visit": "Fri, 10 Sep 2021 17:53:25 GMT",
    "visits": 1
}
```

## GET /leads

Lista todos os Leads por `ordem de visita`, do `maior para o menor`.

## PATCH /leads

Atualiza o valor de "visits" e "lasd_visit" em cada requisição, utilizando o email para encontrar o registro a ser atualizado.

A cada atualização o valor de "visits" é acrescentado em 1.
A cada atualização o valor de last_visit é atualizado para a data do request.

Modelo de requisição:

```python
{
    "email": "john@email.com"
}
```

## DELETE /leads

Deleta um lead específico. O email do lead deve ser usado para encontrar o registro.

```python
{
    "email": "john@email.com"
}
```
