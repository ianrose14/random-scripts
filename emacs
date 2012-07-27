;; global variables/settings

;; Enable backup files.
(setq make-backup-files t)

;; Enable versioning with default values (keep five last versions, I think...)
(setq version-control t)

;; Save all backup file in this directory.
(setq backup-directory-alist (quote ((".*" . "~/.emacs_backups/"))))

;; Delete old versions silently (no prompting)
(setq delete-old-versions t)

;; show column numbers
(setq column-number-mode t)

;; force 80 column width
(setq-default fill-column 80)
(turn-on-auto-fill)

;; automatically indent after hitting RET
(defun my-c-initialization-hook ()
(define-key c-mode-base-map (kbd "RET") 'newline-and-indent))
(add-hook 'c-initialization-hook 'my-c-initialization-hook)

;; For now, use C mode for Go
(setq auto-mode-alist (cons '("\\.go$" . python-mode) auto-mode-alist))

;; Auto Complete Mode
;; http://cx4a.org/software/auto-complete/
(add-to-list 'load-path "~/.emacs.d/auto-complete/")
(require 'auto-complete-config)
(add-to-list 'ac-dictionary-directories "~/.emacs.d/auto-complete/ac-dict")
(ac-config-default)

;; Gocode
(add-to-list 'load-path "~/.emacs.d/")
(require 'go-autocomplete)
(require 'auto-complete-config)
