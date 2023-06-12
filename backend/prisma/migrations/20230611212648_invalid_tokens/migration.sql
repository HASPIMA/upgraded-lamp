/*
  Warnings:

  - Changed the type of `token` on the `tokens` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.

*/
-- AlterTable
ALTER TABLE "tokens" ADD COLUMN     "invalidado" BOOLEAN NOT NULL DEFAULT true,
DROP COLUMN "token",
ADD COLUMN     "token" JSON NOT NULL;
