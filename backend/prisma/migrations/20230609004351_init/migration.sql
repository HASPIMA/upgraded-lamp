-- CreateTable
CREATE TABLE "comics" (
    "id" INTEGER NOT NULL,
    "titulo" VARCHAR(255),
    "descripcion" VARCHAR(255),
    "imagen" VARCHAR(255),

    CONSTRAINT "comics_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "favoritos" (
    "id_usuario" INTEGER NOT NULL,
    "id_comic" INTEGER NOT NULL,

    CONSTRAINT "favoritos_pkey" PRIMARY KEY ("id_usuario","id_comic")
);

-- CreateTable
CREATE TABLE "tokens" (
    "id" SERIAL NOT NULL,
    "token" VARCHAR(255),
    "id_usuario" INTEGER,

    CONSTRAINT "tokens_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "usuarios" (
    "id" SERIAL NOT NULL,
    "nombre" VARCHAR(255),
    "telefono" VARCHAR(255),
    "identificacion" VARCHAR(255),
    "correo_electronico" VARCHAR(255),
    "contrasena" VARCHAR(255),

    CONSTRAINT "usuarios_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "favoritos" ADD CONSTRAINT "favoritos_id_comic_fkey" FOREIGN KEY ("id_comic") REFERENCES "comics"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "favoritos" ADD CONSTRAINT "favoritos_id_usuario_fkey" FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "tokens" ADD CONSTRAINT "tokens_id_usuario_fkey" FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id") ON DELETE CASCADE ON UPDATE CASCADE;
