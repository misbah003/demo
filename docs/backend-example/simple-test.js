// Simple test
require('dotenv').config();
const nodemailer = require('nodemailer');

console.log('Nodemailer type:', typeof nodemailer);
console.log('Nodemailer keys:', Object.keys(nodemailer));
console.log('createTransporter exists?', typeof nodemailer.createTransporter);
console.log('Gmail user:', process.env.GMAIL_USER);
console.log('App password set?', !!process.env.GMAIL_APP_PASSWORD);