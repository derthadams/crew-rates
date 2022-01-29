module.exports = {
    rootDir: '.',
    testEnvironment: "jsdom",
    transform: {
        '^.+\.(js|jsx)?$': 'babel-jest',
        'node_modules\\/little-state-machine.+\.(js|jsx|ts|tsx)?$': 'ts-jest',
        // 'node_modules/little-state-machine/src/.+\\.(js|jsx|tsx)?$': 'ts-jest',
        // 'node_modules/little-state-machine-devtools/dist/.+\\.(js|jsx|tsx)?$': 'ts-jest',


    },
    testMatch: [
        '<rootDir>/frontend/src/**/*.test.{js, jsx}',
        '<rootDir>/frontend/test/**/*.test.js'
    ],
    moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'node'],
    preset: 'ts-jest',
    testPathIgnorePatterns: ['/node_modules/', '/public/'],
    setupFilesAfterEnv: [
        '@testing-library/jest-dom/extend-expect',
    ],
    moduleNameMapper: {
        "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/__mocks__/fileMock.js",
        '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    },
    transformIgnorePatterns: [
        "node_modules\\/(?!little-state-machine).*",
        // "node_modules/(?!little-state-machine-devtools/.*)",
        // 'node_modules/.+',

    ]
}