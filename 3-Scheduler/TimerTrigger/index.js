const nodemailer = require("nodemailer");

module.exports = async function (context, myTimer) {
  // Vytvořte dočasný účet.
  let testAcc = await nodemailer.createTestAccount();

  // Vytvořte znovupoužitelný transporter
  let transporter = nodemailer.createTransport({
    host: "smtp.ethereal.email",
    port: 587,
    secure: false, // true pro 465, false pro všechny ostatní porty
    auth: {
      user: testAcc.user, // generované ethereal username
      pass: testAcc.pass, // generované ethereal heslo
    },
  });

  // Zaslání mailu
  let messageInfo = await transporter.sendMail({
    from: '"Examle" <foo@example.com>', // Zobrazovaná emailová adresa odesílatele
    to: "bar@example.com, baz@example.com", // Seznam příjemců
    subject: "Example email", // Subject
    text: "Hello world", // Kontent emailu
  });

  // Preview emailu je možné pouze s ethereal.email
  console.log("Preview URL: %s", nodemailer.getTestMessageUrl(messageInfo));
};
