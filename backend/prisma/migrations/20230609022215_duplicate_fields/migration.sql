/*
  Warnings:

  - You are about to drop the column `telefono` on the `usuarios` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[identificacion]` on the table `usuarios` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[correo_electronico]` on the table `usuarios` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "usuarios" DROP COLUMN "telefono";

-- CreateIndex
CREATE UNIQUE INDEX "usuarios_identificacion_key" ON "usuarios"("identificacion");

-- CreateIndex
CREATE UNIQUE INDEX "usuarios_correo_electronico_key" ON "usuarios"("correo_electronico");
