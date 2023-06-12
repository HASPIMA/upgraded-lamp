/*
  Warnings:

  - Made the column `titulo` on table `comics` required. This step will fail if there are existing NULL values in that column.
  - Made the column `descripcion` on table `comics` required. This step will fail if there are existing NULL values in that column.
  - Made the column `imagen` on table `comics` required. This step will fail if there are existing NULL values in that column.
  - Made the column `token` on table `tokens` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `salt` to the `usuarios` table without a default value. This is not possible if the table is not empty.
  - Made the column `nombre` on table `usuarios` required. This step will fail if there are existing NULL values in that column.
  - Made the column `identificacion` on table `usuarios` required. This step will fail if there are existing NULL values in that column.
  - Made the column `correo_electronico` on table `usuarios` required. This step will fail if there are existing NULL values in that column.
  - Made the column `contrasena` on table `usuarios` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "comics" ALTER COLUMN "titulo" SET NOT NULL,
ALTER COLUMN "descripcion" SET NOT NULL,
ALTER COLUMN "imagen" SET NOT NULL;

-- AlterTable
ALTER TABLE "tokens" ALTER COLUMN "token" SET NOT NULL;

-- AlterTable
ALTER TABLE "usuarios" ADD COLUMN     "salt" VARCHAR(255) NOT NULL,
ALTER COLUMN "nombre" SET NOT NULL,
ALTER COLUMN "identificacion" SET NOT NULL,
ALTER COLUMN "correo_electronico" SET NOT NULL,
ALTER COLUMN "contrasena" SET NOT NULL;
