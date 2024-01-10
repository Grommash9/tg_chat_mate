echo "Running TypeScript linting"
cd typescript-app
npm install
npx prettier --check --ignore-path .prettierignore frontend app.ts
echo "TypeScript linting completed successfully"