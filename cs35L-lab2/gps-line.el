(defun gps-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((n (line-number-at-pos)) (l(count-matches "\n" (point-min)(point-max))))
        (message "Line %d%s%d" n"/"l)
      ))
