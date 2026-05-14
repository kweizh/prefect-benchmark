from prefect.blocks.system import Secret

Secret(value="super-secret-value").save(name="my-api-key", overwrite=True)
