db.createUser({
    user: " admin",
    pwd: "pwd",
    roles: [
      { role: "readWrite", db: "Project_Python" }
    ]
  });